import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Walker, Group, Route, Event
from auth import AuthError, requires_auth

ITEMS_PER_PAGE = 10


def paginate_items(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    item = [item.format() for item in selection]
    current_item = item[start:end]

    return current_item


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  Set up CORS. Allow '*' for origins.
  '''
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    '''
  Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # Root Message
    @app.route('/')
    def root():

        return jsonify({
            'message': 'WFM_API'
        })

    # ---------------------------------------------------
    # Walkers - details of walkers registered on the site
    # ---------------------------------------------------

    # GET details for all walkers
    @app.route('/walkers')
    @requires_auth('read:walkers')
    def retrieve_walkers(payload):
        try:
            print("Getting walker info")
            walkers = list(map(Walker.format,
                               Walker.query.order_by(Walker.id).all()))
            print(walkers)

            if len(walkers) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'walkers': walkers
            })
        except Exception as e:
            print(e)
            return jsonify({
                'message': 'Error getting walker information'
            })

    # GET details for a single a walker

    @app.route('/walkers/<int:walker_id>', methods=['GET'])
    @requires_auth('read:walkers')
    def get_walker_details(payload, walker_id):

        print(walker_id)
        walker = Walker.query.filter(Walker.id == walker_id).one_or_none()
        print(walker)
        if walker is None:
            abort(404)

        '''current_questions = paginate_questions(request, selection)'''

        return jsonify({
            'success': True,
            'walker': Walker.format(walker)
        })

    # POST a new walkers details

    @app.route('/walkers/add', methods=['POST'])
    @requires_auth('create:walkers')
    def create_walker(payload):
        body = request.get_json()
        print(body)

        new_first_name = body['first_name']
        new_last_name = body['last_name']
        new_user_name = body['user_name']
        new_age = body['age']
        new_email = body['email']
        new_phone = body['phone']
        new_area = body['area']
        new_sex = body['sex']

        try:
            walker = Walker(
                first_name=new_first_name,
                last_name=new_last_name,
                user_name=new_user_name,
                age=new_age,
                phone=new_phone,
                area=new_area,
                email=new_email,
                sex=new_sex
            )
            print(walker)
            walker.insert()

            walkers = list(map(Walker.format,
                               Walker.query.order_by(Walker.id).all()))
            '''current_questions = paginate_questions(request, selection)'''

            return jsonify({
                'success': True,
                'walkers': walkers
            })

        except Exception as e:
            print(e)
            abort(422)

    # DELETE a single walker
    @app.route('/walkers/<int:walker_id>', methods=['DELETE'])
    @requires_auth('delete:walkers')
    def delete_walker(payload, walker_id):
        try:
            print(walker_id)
            walker = Walker.query.filter(Walker.id == walker_id).one_or_none()

            if walker is None:
                abort(404)

            walker.delete()
            '''walkers = Walker.query.order_by(walker_id).all()'''
            '''current_questions = paginate_questions(request, selection)'''

            return jsonify({
                'success': True,
                'deleted': walker_id
            })

        except BaseException:
            abort(422)

    # PATCH - EDIT a walkers details
    @app.route('/walkers/<walker_id>', methods=['PATCH'])
    @requires_auth('edit:walkers')
    def edit_walker(payload, walker_id):
        body = request.get_json()
        walker_to_edit = Walker.query.filter(
            Walker.id == walker_id).one_or_none()
        print(walker_to_edit)
        print(body)

        if walker_to_edit:
            try:
                walker_to_edit.first_name = body.get('first_name')
                walker_to_edit.last_name = body.get('last_name')
                walker_to_edit.user_name = body.get('user_name')
                walker_to_edit.age = body.get('age')
                walker_to_edit.phone = body.get('phone')
                walker_to_edit.area = body.get('area')
                walker_to_edit.email = body.get('email')
                walker_to_edit.sex = body.get('sex')

                walker_to_edit.update()

                return jsonify({
                    'success': True,
                    'walker': walker_id
                })

            except BaseException:
                abort(422)

        else:
            abort(404)

    # ---------------------------------------------------
    # Groups - details of groups of walkers on the site
    # ---------------------------------------------------

    # Get details of all groups
    @app.route('/groups')
    def retrieve_groups():
        try:
            print("Getting group info")
            groups = list(map(Group.format,
                              Group.query.order_by(Group.group_name).all()))
            print(groups)

            if len(groups) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'groups': groups
            })
        except Exception as e:
            print(e)
            return jsonify({
                'message': 'Error'
            })

    # GET details for a single a group
    @app.route('/groups/<int:group_id>', methods=['GET'])
    def get_group_details(group_id):

        print(group_id)
        group = Group.query.filter(Group.id == group_id).one_or_none()
        print(group)
        if group is None:
            abort(404)

        '''current_questions = paginate_questions(request, selection)'''

        return jsonify({
            'success': True,
            'group': Group.format(group)
        })

    # POST a new group details

    @app.route('/groups/add', methods=['POST'])
    @requires_auth('create:group')
    def create_group(payload):
        body = request.get_json()
        print(body)

        new_group_name = body['group_name']
        new_area = body['area']

        try:
            group = Group(
                group_name=new_group_name,
                area=new_area
            )
            print(group)
            group.insert()

            groups = list(map(Group.format,
                              Group.query.order_by(Group.group_name).all()))
            '''current_questions = paginate_questions(request, selection)'''

            return jsonify({
                'success': True,
                'walkers': groups
            })

        except Exception as e:
            print(e)
            abort(422)

    # DELETE a single group
    @app.route('/groups/<int:group_id>', methods=['DELETE'])
    @requires_auth('delete:group')
    def delete_group(payload, group_id):
        try:
            print(group_id)
            group = Group.query.filter(Group.id == group_id).one_or_none()

            if group is None:
                abort(404)

            group.delete()
            '''walkers = Walker.query.order_by(walker_id).all()'''
            '''current_questions = paginate_questions(request, selection)'''

            return jsonify({
                'success': True,
                'deleted': group_id
            })

        except BaseException:
            abort(422)

    # PATCH - EDIT a groups details
    @app.route('/groups/<group_id>', methods=['PATCH'])
    @requires_auth('edit:group')
    def edit_group(payload, group_id):
        body = request.get_json()
        group_to_edit = Group.query.filter(Group.id == group_id).one_or_none()
        print(group_to_edit)
        print(body)

        if group_to_edit:
            try:
                group_to_edit.group_name = body.get('group_name')
                group_to_edit.area = body.get('area')
                group_to_edit.no_of_members = body.get('no_of_members')

                group_to_edit.update()

                return jsonify({
                    'success': True,
                    'group': group_id
                })

            except BaseException:
                abort(422)

        else:
            abort(404)

    # ---------------------------------------------------
    # Routes - details of routes on the site
    # ---------------------------------------------------

    # GET - Get all routes details
    @app.route('/routes')
    def get_routes():
        try:
            print("Getting route info")
            routes = list(map(Route.format,
                              Route.query.order_by(Route.id).all()))
            print(routes)

            if len(routes) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'routes': routes
            })
        except Exception as e:
            print(e)
            return jsonify({
                'message': 'Error'
            })

    # GET details for a single a route
    @app.route('/routes/<int:route_id>', methods=['GET'])
    def get_route_details(route_id):

        print(route_id)
        route = Route.query.filter(Route.id == route_id).one_or_none()
        print(route)
        if route is None:
            abort(404)

        '''current_questions = paginate_questions(request, selection)'''

        return jsonify({
            'success': True,
            'route': Route.format(route)
        })

    # POST a new route details

    @app.route('/routes/add', methods=['POST'])
    @requires_auth('create:route')
    def create_route(payload):
        body = request.get_json()
        print(body)

        new_route_name = body['route_name']
        new_route_description = body['route_description']
        new_route_difficulty = body['route_difficulty']
        new_map_link = body['map_link']
        new_length = body['length']
        new_area = body['area']

        try:
            route = Route(
                route_name=new_route_name,
                area=new_area,
                route_description=new_route_description,
                route_difficulty=new_route_difficulty,
                map_link=new_map_link,
                length=new_length
            )
            print(route)
            route.insert()

            routes = list(map(Route.format,
                              Route.query.order_by(Route.route_name).all()))
            '''current_questions = paginate_questions(request, selection)'''

            return jsonify({
                'success': True,
                'routes': routes
            })

        except Exception as e:
            print(e)
            abort(422)

    # DELETE a single route
    @app.route('/routes/<int:route_id>', methods=['DELETE'])
    @requires_auth('delete:route')
    def delete_route(payload, route_id):
        try:
            print(route_id)
            route = Route.query.filter(Route.id == route_id).one_or_none()

            if route is None:
                abort(404)

            route.delete()
            '''walkers = Walker.query.order_by(walker_id).all()'''
            '''current_questions = paginate_questions(request, selection)'''

            return jsonify({
                'success': True,
                'deleted': route_id
            })

        except BaseException:
            abort(422)

    # PATCH - EDIT a routes details
    @app.route('/routes/<route_id>', methods=['PATCH'])
    @requires_auth('edit:route')
    def edit_route(payload, route_id):
        body = request.get_json()
        route_to_edit = Route.query.filter(Route.id == route_id).one_or_none()
        print(route_to_edit)
        print(body)

        if route_to_edit:
            try:
                route_to_edit.route_name = body.get('route_name')
                route_to_edit.area = body.get('area')
                route_to_edit.route_description = body.get('route_description')
                route_to_edit.route_difficulty = body.get('route_difficulty')
                route_to_edit.map_link = body.get('map_link')
                route_to_edit.length = body.get('length')

                route_to_edit.update()

                return jsonify({
                    'success': True,
                    'route': route_id
                })

            except BaseException:
                abort(422)

        else:
            abort(404)

    # ---------------------------------------------------
    # Events - details of events on the site
    # ---------------------------------------------------

    # GET - Get all event details
    @app.route('/events')
    def get_events():
        try:
            print("Getting event info")
            events = list(map(Event.format,
                              Event.query.order_by(Event.id).all()))
            print(events)

            if len(events) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'events': events
            })
        except Exception as e:
            print(e)
            return jsonify({
                'message': 'Error'
            })

    # GET details for a single a event
    @app.route('/events/<int:event_id>', methods=['GET'])
    def get_event_details(event_id):

        print(event_id)
        event = Event.query.filter(Event.id == event_id).one_or_none()
        print(event)
        if event is None:
            abort(404)

        '''current_questions = paginate_questions(request, selection)'''

        return jsonify({
            'success': True,
            'event': Event.format(event)
        })

    # POST a new event details

    @app.route('/events/add', methods=['POST'])
    @requires_auth('create:event')
    def create_event(payload):
        body = request.get_json()
        print(body)

        new_route_id = body['route_id']
        new_date_time = body['date_time']

        try:
            event = Event(
                route_id=new_route_id,
                date_time=new_date_time
            )
            print(event)
            event.insert()

            events = list(map(Event.format,
                              Event.query.order_by(Event.id).all()))
            '''current_questions = paginate_questions(request, selection)'''

            return jsonify({
                'success': True,
                'events': events
            })

        except Exception as e:
            print(e)
            abort(422)

    # DELETE a single route
    @app.route('/events/<int:event_id>', methods=['DELETE'])
    @requires_auth('delete:route')
    def delete_event(payload, event_id):
        try:
            print(event_id)
            event = Event.query.filter(Event.id == event_id).one_or_none()

            if event is None:
                abort(404)

            event.delete()
            '''walkers = Walker.query.order_by(walker_id).all()'''
            '''current_questions = paginate_questions(request, selection)'''

            return jsonify({
                'success': True,
                'deleted': event_id
            })

        except BaseException:
            abort(422)

    # PATCH - EDIT an events details
    @app.route('/events/<event_id>', methods=['PATCH'])
    @requires_auth('edit:event')
    def edit_event(payload, event_id):
        body = request.get_json()
        event_to_edit = Event.query.filter(Event.id == event_id).one_or_none()
        print(event_to_edit)
        print(body)

        if event_to_edit:
            try:
                event_to_edit.route_id = body.get('route_id')
                event_to_edit.date_time = body.get('date_time')

                event_to_edit.update()

                return jsonify({
                    'success': True,
                    'event': event_id
                })

            except BaseException:
                abort(422)

        else:
            abort(404)

    '''
  A POST endpoint to get walkers based on a search term.
  '''
    @app.route('/walkers/search', methods=['POST'])
    def search_walker():
        body = request.get_json()
        search = body.get('searchTerm', '')
        print(search)
        print("Searching")
        try:

            walkers = Walker.query.filter(
                Walker.first_name.ilike(
                    '%' + search + '%')).all()

            if len(walkers) == 0:
                abort(404)

            '''current_questions = paginate_questions(request, questions)'''

            return jsonify({
                'success': True,
                'walkers': walkers,
            })

        except BaseException:
            abort(422)

    # ---------------------------------------------------
    # Error Handlers
    # ---------------------------------------------------

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request",
            "error message": str(error)
        }), 400

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

    @app.errorhandler(AuthError)
    def autherror(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), 401

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
