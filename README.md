#### Walking from Home

With the emergence of Hybrid and more flexible working post covid, the importance of social interaction and physical excersize becomes even more important for home workers. Walking From Home will offer a platform for home workers to share walking routes, form walking groups and arrange to meet for one off or regular walks.

The API provides the backend for the website and is hosted in Heroku.

A very basic front end has been developed using Vuetify, Vue and Veuex. This is hosted in Firebase.


## Getting Started

### Backend dependencies, local development and hosting

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the project root directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the wfh.psql file provided. From the backend folder in terminal run:
```bash
psql wfh < wfh.psql
```

## Running the server

From within the root directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export DATABASE_URL = "postgres://postgres@localhost:5432/wfh" or your local postgres server details
export FLASK_APP=app.py;
flask run --reload
```

### Backend API Hosting

#### Heroku Endpoint

The backend can be accessed at https://walkingfromhome.herokuapp.com/

#### Endpoints

There a are four main endpoints for the API

/walkers    contains details of the registered walkers
/groups     contains details of groups of walkers
/routes     contains details of the walking routes
/events     contains details of walking events

The endpoints are explained in more detail below.

#### Authentication

Authentication is handled by Auth0. The site will not show any details unless the user has regstered. Further functionality is restricted by the application of user roles. There are two roles WFH-User and WFH-Admin. The admin role allows full permissions to create, edit, delete on all endpoints.

Two test accounts have been setup:-

wfhuser@gmail.com - which is assigned the WFH-User role
wfhadmin@gmail.com - which is assigned the WFH-Admin role

both users have password WalkingFromH0me!

### Front End Hosting

A basic front end has been developed to show the login page and redirection working and very basic restriction of data access. You can only view each section if you are logged in.

The front end can be found at https://walking-from-home.web.app/

Press the login button top left and use the credentials above.

From the menu select Profile to view the persmissions for each user extracted from the Auth0 JWT.

#### API

### Authentication

Authentication is required view Walker information all other endpoints do not require auth.

If an an authorized request is made it will result in a

```{"error":404,"error message":"404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.","message":"resource not found","success":false}
```

### Error Handling

Errors are returned as JSON objects in the following format:

```{
      "success": False,
      "error": 404,
      "message": "resource not found",
      "error message": str(error)
    }
```

The API will return the following error types when requests fail:

- 400 - bad request
- 404 - resource not found
- 405 - method not allowed
- 422 - unprocessable

### Endpoints

## Walkers

# GET /walkers

- General:
    - Returns a list of walkers, success value
    - Sample: ```curl https://walkingfromhome.herokuapp.com/walkers```

```
{
    "walkers": [{
        "id": "1",
        "first_name": "Rob",
        "last_name": "Wilson",
        "user_name": "robwil",
        "age": "14",
        "sex": "Male"
        "email": "anemailaddres@email.com,
        "phone", "0009090393
        "area", "AL87ED
    }],
    "success": true
}
```

# GET /walkers/1

- General:
    - Returns a single walker by id number, success value
    - Sample: ```curl https://walkingfromhome.herokuapp.com/walkers/1```

```
{
    "walker": {
        "id": "1",
        "first_name": "Rob",
        "last_name": "Wilson",
        "user_name": "robwil",
        "age": "14",
        "sex": "Male"
        "email": "anemailaddres@email.com,
        "phone", "0009090393
        "area", "AL87ED
    },
    "success": true
}
```

# POST /walkers/add

- General:
    - Returns a list of walkers, success value 
    - Sample: ```curl   --header "Content-Type: application/json" \
                        --request POST \
                        --data '{
                                 "id": "1",
                                 "first_name": "Rob",
                                 "last_name": "Wilson",
                                 "user_name": "robwil",
                                 "age": "14",
                                 "sex": "Male"
                                 "email": "anemailaddres@email.com,
                                 "phone", "0009090393
                                 "area", "AL87ED
                              }' \
                        https://walkingfromhome.herokuapp.com/walkers/add

```
{
    "walkers": [{
        "id": "1",
        "first_name": "Rob",
        "last_name": "Wilson",
        "user_name": "robwil",
        "age": "14",
        "sex": "Male"
        "email": "anemailaddres@email.com,
        "phone", "0009090393
        "area", "AL87ED
    }],
    "success": true
}
```

# PATCH /walkers/

- General:
    - Returns a list of walkers, success value 
    - Sample: ```curl   --header "Content-Type: application/json" \
                        --request PATCH \
                        --data '{
                                 "id": "1",
                                 "first_name": "Rob",
                                 "last_name": "Wilson",
                                 "user_name": "robwil",
                                 "age": "14",
                                 "sex": "Male"
                                 "email": "anemailaddres@email.com,
                                 "phone", "0009090393
                                 "area", "AL87ED
                              }' \
                        https://walkingfromhome.herokuapp.com/walkers

```
{
    "walkers": [{
        "id": "1",
        "first_name": "Rob",
        "last_name": "Wilson",
        "user_name": "robwil",
        "age": "14",
        "sex": "Male"
        "email": "anemailaddres@email.com,
        "phone", "0009090393
        "area", "AL87ED
    }],
    "success": true
}
```

# DELETE /walkers/

- General:
    - Deletes a walkers details , success value 
    - Sample: ```curl -X DELETE https://walkingfromhome.herokuapp.com/walkers/10```

```
{
    "walker": id
    "success": true
}
```

## Groups

# GET /groups

- General:
    - Returns a list of groups, success value
    - Sample: ```curl https://walkingfromhome.herokuapp.com/groups```

```
{
    {"groups":[{"area":"AL71AP","group_name":"Hatfield","id":2,"no_of_members":5}],
    "success": true
}
```

# POST /groupss/add

- General:
    - Returns a list of groups, success value 
    - Sample: ```curl   --header "Content-Type: application/json" \
                        --request POST \
                        --data '{"area":"AL71AP","group_name":"Hatfield","id":2,"no_of_members":5' \
                        https://walkingfromhome.herokuapp.com/groups/add

```
{
    "groups":[{"area":"AL71AP","group_name":"Hatfield","id":2,"no_of_members":5}],
    "success": true
}
```

# PATCH /groups/

- General:
    - Returns a list of groupss, success value 
    - Sample: ```curl   --header "Content-Type: application/json" \
                        --request PATCH \
                        --data '"groups":[{"area":"AL71AP","group_name":"Hatfield","id":2,"no_of_members":5}' \
                        https://walkingfromhome.herokuapp.com/groups/

```
{
    "walkers": ["groups":[{"area":"AL71AP","group_name":"Hatfield","id":2,"no_of_members":5}],
    "success": true
}
```

# DELETE /groups/

- General:
    - Deletes a groups details , success value 
    - Sample: ```curl -X DELETE https://walkingfromhome.herokuapp.com/groups/10```

```
{
    "group": id
    "success": true
}
```


## Routes

# GET /routes

- General:
    - Returns a list of routes, success value
    - Sample: ```curl https://walkingfromhome.herokuapp.com/routes```

```
{
    {"routes":[{"area":"AL87ED","id":1,"length":5.2,"map_link":"https://www.google.com/maps/d/u/0/edit?mid=1Nh6wsnIK52fNbYgndi595jysVlasE6W-&usp=sharing","route_description":"Short 5km route","route_difficulty":"Easy","route_name":"Sherrads Woods"},
    "success": true
}
```

# POST /routes/add

- General:
    - Returns a list of routes, success value 
    - Sample: ```curl   --header "Content-Type: application/json" \
                        --request POST \
                        --data '{"area":"AL87ED","id":1,"length":5.2,"map_link":"https://www.google.com/maps/d/u/0/edit?mid=1Nh6wsnIK52fNbYgndi595jysVlasE6W-&usp=sharing","route_description":"Short 5km route","route_difficulty":"Easy","route_name":"Sherrads Woods"} \
                        https://walkingfromhome.herokuapp.com/routes/add

```
{
    "routes":[{"area":"AL87ED","id":1,"length":5.2,"map_link":"https://www.google.com/maps/d/u/0/edit?mid=1Nh6wsnIK52fNbYgndi595jysVlasE6W-&usp=sharing","route_description":"Short 5km route","route_difficulty":"Easy","route_name":"Sherrads Woods"}],
    "success": true
}
```

# PATCH /routes/

- General:
    - Returns a list of routes, success value 
    - Sample: ```curl   --header "Content-Type: application/json" \
                        --request PATCH \
                        --data '"routes":[{"area":"AL87ED","id":1,"length":5.2,"map_link":"https://www.google.com/maps/d/u/0/edit?mid=1Nh6wsnIK52fNbYgndi595jysVlasE6W-&usp=sharing","route_description":"Short 5km route","route_difficulty":"Easy","route_name":"Sherrads Woods"}' \
                        https://walkingfromhome.herokuapp.com/routes/

```
{
    "routes": ["routes":[{"area":"AL87ED","id":1,"length":5.2,"map_link":"https://www.google.com/maps/d/u/0/edit?mid=1Nh6wsnIK52fNbYgndi595jysVlasE6W-&usp=sharing","route_description":"Short 5km route","route_difficulty":"Easy","route_name":"Sherrads Woods"}],
    "success": true
}
```

# DELETE /routes/

- General:
    - Deletes a routes details , success value 
    - Sample: ```curl -X DELETE https://walkingfromhome.herokuapp.com/routes/10```

```
{
    "route": id
    "success": true
}
```

## Events

# GET /events

- General:
    - Returns a list of events, success value
    - Sample: ```curl https://walkingfromhome.herokuapp.com/events```

```
{
    {"events":[{"date_time":"23/04/2021","id":1,"route_id":2},
    "success": true
}
```

# POST /events/add

- General:
    - Returns a list of events, success value 
    - Sample: ```curl   --header "Content-Type: application/json" \
                        --request POST \
                        --data '{"date_time":"23/04/2021","id":1,"route_id":2} \
                        https://walkingfromhome.herokuapp.com/events/add

```
{
    "events":[{"date_time":"23/04/2021","id":1,"route_id":2}],
    "success": true
}
```

# PATCH /events/

- General:
    - Returns a list of events, success value 
    - Sample: ```curl   --header "Content-Type: application/json" \
                        --request PATCH \
                        --data '"events":[{"date_time":"23/04/2021","id":1,"route_id":2}' \
                        https://walkingfromhome.herokuapp.com/events/

```
{
    "events": ["events":[{"date_time":"23/04/2021","id":1,"route_id":2}],
    "success": true
}
```

# DELETE /events/

- General:
    - Deletes a events details , success value 
    - Sample: ```curl -X DELETE https://walkingfromhome.herokuapp.com/events/10```

```
{
    "route": id
    "success": true
}
```
