import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES
'''
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        drinks_short = Drink.query.all()
        print(drinks_short)
        return jsonify({
            'success': True,
            'drinks': [drink.short() for drink in drinks_short]
        }) 

    except:
        abort(404)

'''
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    try:
        drinks_long = Drink.query.all()

        return jsonify({
            'success': True,
            'drinks': [drink.long() for drink in drinks_long]
        }) 

    except:
        abort(404)


'''
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(payload):
    body = request.get_json()
    print(body)
    if not body:
        abort(422)

    new_title = body['title']
    new_recipe = body['recipe']

    try:
        new_drink = Drink(title = new_title, recipe=json.dumps(new_recipe))
        new_drink.insert()

        return jsonify({
            'success': True,
            'drinks': [new_drink.long()]
        }) 

    except:
        abort(404)


'''
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drink(payload, id):

    drink_to_edit = Drink.query.get(id)

    if drink_to_edit:
        try:
            body = request.get_json()
            edit_title = body.get('title')
            edit_recipe = body.get('recipe')
            if edit_title:
                drink_to_edit.title = edit_title
            if edit_recipe:
                drink_to_edit.recipe = edit_recipe
    
            drink_to_edit.update()

            return jsonify({
                'success': True,
                'drinks': [drink_to_edit.long()]
            }) 

        except:
            abort(422)

    else:
        abort(404)

'''
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):

    drink_to_delete = Drink.query.get(id)

    if drink_to_delete:
        try:
            drink_to_delete.delete()

            return jsonify({
                'success': True,
                'delete': id
            }) 
        
        except:
            abort(422)

    else:
        abort(404)

# Error Handling

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request",
        "error message": str(error)
    }), 400

@app.errorhandler(403)  
def not_found(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "unathorised",
        "error message": str(error)
    }), 404

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found",
        "error message": str(error)
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed",
        "error message": str(error)
    }), 405

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable",
        "error message": str(error)
    }), 422

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(AuthError)
def autherror(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error
    }), 401
