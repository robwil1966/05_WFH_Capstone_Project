import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Walker, Group, Route, Event


class WFHTestCase(unittest.TestCase):
    """This class represents the walking from home test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "wfh"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
        # A test walker
        self.new_walker = {
                                "age": 55,
                                "area": "AL87ED",
                                "email": "thewilbos@gmail.com",
                                "first_name": "Rob",
                                "id": 2,
                                "last_name": "Wilson",
                                "phone": "07960086837",
                                "sex": "M",
                                "user_name": "robwil1966"
                            }
        # A test group
        self.new_group = {
                            "group_name": "The Oldies",
                            "area": "AL87ED"
                        }
        
        # A test route
        self._new_route = {
                                "route_name": "WGC 100",
                                "area": "AL87ED",
                                "length": 10,
                                "map_link": "",
                                "route_difficulty": "Hard",
                                "route_description": "WGC 100 Walk"
                            }

        # A test event
        self.new_event = {
                                "route_id": "1",
                                "date_time": "20/10/2021"
                            }
        self.user_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlVYX1F3TGdfYUJMbGRaUTVaSHMtVyJ9.eyJpc3MiOiJodHRwczovL2Rldi1ybnp1OGwzZy5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA4YzBmNmZhZmM1NWUwMDY5NmE4MGEzIiwiYXVkIjoid2ZoIiwiaWF0IjoxNjIxMzM4OTg3LCJleHAiOjE2MjEzNDYxODcsImF6cCI6IjNRa3NDc0ZKNTRnSVpTSUZJc1h0S0JqYTF6elJ5OEg3Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJjcmVhdGU6ZXZlbnQiLCJjcmVhdGU6Z3JvdXAiLCJjcmVhdGU6cm91dGUiLCJkZWxldGU6ZXZlbnQiLCJkZWxldGU6Z3JvdXAiLCJkZWxldGU6cm91dGUiLCJlZGl0OmV2ZW50IiwiZWRpdDpncm91cCIsImVkaXQ6cm91dGUiLCJlZGl0OndhbGtlcnMiLCJyZWFkOmdyb3VwIiwicmVhZDp3YWxrZXJzIiwidXBkYXRlOndhbGtlcnMiXX0.DvgIDHZelacPBWDcAmGEYqQr7fAA7lUQold7PfavJyedQw1FHLWO-JKWQ-1tHICAtGrFV85bSz--nW8VCpcGmSa2mJ5NmHek3FHdZqcXYtT5XYs0ma_QVqxSw148G8DVtnku5xDdnxVGa5_n18g47t1EyJJAmAlfh486KLvpoLvBUXJad9ZPV3bHjH6PfUq53xXqTu8eGSovEPQ56ZYTudHkhT7AyHk52KIJNwxPr1dN_-c8NVm6hjxrwao4erHMUe74uTF9IYGpzCA8w_Qb7156sQ9ysfF2_8HeAZ9X1ZimPei5NdgOqLz7uTxt94bv0biR2tLxnZUPTK2SLXo4Hw"

    ### Walker Tests ###

    ## Test Get Walkers ##
    # Should fail without authentication #
    def test_get_Walkers_noAuth(self):
        print("Testing Get Walkers No Auth")
        res = self.client().get('/walkers')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # Should pass with valid autentication token  #
    def test_get_Walkers_auth(self):
        print("Testing Get Walkers with Auth")

        authorization = 'Bearer ' + self.user_token
        headers = {
            'Authorization': authorization
        }
        print(headers)
        res = self.client().get('/walkers', headers = headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Should pass with valid autentication token  #
    def test_get_Walker_auth(self):
        print("Testing Get Walker with Auth")

        authorization = 'Bearer ' + self.user_token
        headers = {
            'Authorization': authorization
        }
        print(headers)
        res = self.client().get('/walkers/13', headers = headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    ## Test if walker does not exist
    def test_get_walker_does_not_exist(self):
        authorization = 'Bearer ' + self.user_token
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json',
            'Authorization': authorization
        }
        res = self.client().get('/walkers/1000', headers = headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertTrue(data['message'], 'resource not found') 

    ### Group Tests ###

    # Should pass as does not require auth #
    def test_get_Group(self):
        print("Testing Get Group No Auth")
        res = self.client().get('/groups')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Add group should pass with valid autentication token  #
    def test_add_Group_auth(self):
        print("Testing Add Group with Auth")

        authorization = 'Bearer ' + self.user_token
        headers = {
            'Authorization': authorization
        }
        print(headers)
        res = self.client().post('/groups/add', headers = headers, json = {"group_name": "The Oldies",
                            "area": "AL87ED"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Add event should fail without a valid autentication token  #
    def test_get_Group_no_auth(self):
        print("Testing Add Group without Auth")

        authorization = 'Bearer ' + self.user_token
        headers = {
            'Authorization': authorization
        }
        print(headers)
        res = self.client().post('/groups/add', json = {"group_name": "The Oldies",
                            "area": "AL87ED"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    ## Test if event does not exist
    def test_get_Group_does_not_exist(self):
        authorization = 'Bearer ' + self.user_token
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json',
            'Authorization': authorization
        }
        res = self.client().get('/groups/1000', headers = headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertTrue(data['message'], 'resource not found') 


    ### Event Tests ###

    # Should pass as does not require auth #
    def test_get_Event(self):
        print("Testing Get Event No Auth")
        res = self.client().get('/events')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Add event should pass with valid autentication token  #
    def test_add_Event_auth(self):
        print("Testing Add Event with Auth")

        authorization = 'Bearer ' + self.user_token
        headers = {
            'Authorization': authorization
        }
        print(headers)
        res = self.client().post('/events/add', headers = headers, json = {"route_id": "1",
                                "date_time": "20/10/2021"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Add event should fail without a valid autentication token  #
    def test_get_Event_no_auth(self):
        print("Testing Add Event without Auth")

        authorization = 'Bearer ' + self.user_token
        headers = {
            'Authorization': authorization
        }
        print(headers)
        res = self.client().post('/events/add', json = {"route_id": "1", "date_time": "20/10/2021"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    ## Test if event does not exist
    def test_get_event_does_not_exist(self):
        authorization = 'Bearer ' + self.user_token
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json',
            'Authorization': authorization
        }
        res = self.client().get('/events/1000', headers = headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertTrue(data['message'], 'resource not found') 

    ### Route Tests ###

    # Should pass as does not require auth #
    def test_get_Route(self):
        print("Testing Get Event No Auth")
        res = self.client().get('/routes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Add event should pass with valid autentication token  #
    def test_add_Route_auth(self):
        print("Testing Add Route with Auth")

        authorization = 'Bearer ' + self.user_token
        headers = {
            'Authorization': authorization
        }
        print(headers)
        res = self.client().post('/routes/add', headers = headers, json = {"route_name": "WGC 100",
                                "area": "AL87ED",
                                "length": 10,
                                "map_link": "",
                                "route_difficulty": "Hard",
                                "route_description": "WGC 100 Walk"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Add event should fail without a valid autentication token  #
    def test_get_Route_no_auth(self):
        print("Testing Add Event without Auth")

        authorization = 'Bearer ' + self.user_token
        headers = {
            'Authorization': authorization
        }
        print(headers)
        res = self.client().post('/events/add', json = {"route_name": "WGC 100",
                                "area": "AL87ED",
                                "length": 10,
                                "map_link": "",
                                "route_difficulty": "Hard",
                                "route_description": "WGC 100 Walk"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    ## Test if event does not exist
    def test_get_Route_does_not_exist(self):
        authorization = 'Bearer ' + self.user_token
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json',
            'Authorization': authorization
        }
        res = self.client().get('/routes/1000', headers = headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertTrue(data['message'], 'resource not found') 




    
    def tearDown(self):
        """Executed after reach test"""
        pass


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()