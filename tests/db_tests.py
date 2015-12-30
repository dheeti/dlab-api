import os
import json
import unittest
import sys
import uuid

import py2neo


# add parent directory to path to import app
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)


from app import app, graph


class UserTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        # create random username
        self.user = "testuser-{0}".format(uuid.uuid4())
        self.endpoint = "/api/user"
        self.data = dict(username=self.user, name="Test", city="Portland")

    def test_create_new(self):
        # make sure user does not exist
        graph.delete_user(self.user)

        # submit POST request to create new user
        rv = self.app.post(self.endpoint, data=self.data)
        
        # confirm JSON response matches what we expect
        response = json.loads(rv.data)
        expected = dict(
            node_id=self.user,
            success="User <{0}> created".format(self.user)
        )
        self.assertEqual(response, expected)
        
        # query graph directly and verify node exists
        node = graph.find_node("User", self.user)
        self.assertEqual(node.properties["node_id"], self.user)
   
        # clean up
        graph.delete_user(self.user)

    def test_create_existing(self):
        # make sure user exists
        graph.create_user(self.data)
        
        # submit POST request to create a user that already exists
        rv = self.app.post(self.endpoint, data=self.data)

        # confirm JSON response matches what we expect
        response = json.loads(rv.data)
        expected = dict(
            node_id=self.user,
            error="User <{0}> already exists".format(self.user)
        )
        self.assertEqual(response, expected)

        # clean up
        graph.delete_user(self.user)

       
    def test_get_user(self):
        # make sure user exists
        graph.create_user(self.data)

        # submit GET request to retrieve user data
        rv = self.app.get("/api/user", data=dict(id=self.user))
        
        # confirm JSON response matches what we expect
        response = json.loads(rv.data)
        expected = dict(
            id=self.user,
            name=self.data["name"],
            city=self.data["city"]
        )
        self.assertEqual(response, expected)
           
        # clean up
        graph.delete_user(self.user)


class UserRankTests(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.endpoint = "/api/value"
        
        # make sure user exists
        self.user = "testuser-{0}".format(uuid.uuid4())
        self.node = "v1"
        self.rank1 = 1
        self.rank2 = 2
        self.user_data = dict(username=self.user, name="Test", city="Portland")
        graph.create_user(self.user_data)
        self.data = dict(user_id="", node_id="", rank=self.rank1, issue_id='i1')

    def tearDown(self):
        user = graph.find_node("User", self.user)
        node = graph.find_node("Value", self.node)
        graph.delete_link(user, node, "RANKS")
        graph.delete_user(self.user)

    def test_valid_rank(self):
        data = dict(self.data)
        data["user_id"] = self.user
        data["node_id"] = self.node
        rv = self.app.post(self.endpoint, data=data)
        expected = dict(success=True)
        self.check_status_code(rv.status_code)
        self.check_response(expected, rv.data)
        self.check_rank(self.rank1)

    def test_invalid_rank_no_user(self):
        data = dict(self.data)
        data["user_id"] = uuid.uuid4()
        data["node_id"] = self.node 
        rv = self.app.post(self.endpoint, data=data)
        expected = dict(success=False, error="invalid user_id")
        self.check_status_code(rv.status_code)
        self.check_response(expected, rv.data)

    def test_invalid_rank_no_node(self):
        # invalid rank request, node does not exist
        data = dict(self.data)
        data["user_id"] = self.user
        data["node_id"] = uuid.uuid4()
        rv = self.app.post(self.endpoint, data=data)
        expected = dict(success=False, error="invalid node_id")
        self.check_status_code(rv.status_code)
        self.check_response(expected, rv.data)
    
    def test_update_rank(self):
        # rank a node then update the ranking
        data = dict(self.data)
        data["user_id"] = self.user
        data["node_id"] = self.node 
        
        # rank node initially
        rv = self.app.post(self.endpoint, data=data)
        self.check_status_code(rv.status_code)
        expected = dict(success=True)
        self.check_response(expected, rv.data)
        self.check_rank(self.rank1)

        # update rank
        data["rank"] = self.rank2
        rv = self.app.post(self.endpoint, data=data)
        self.check_status_code(rv.status_code)
        expected = dict(success=True)
        self.check_response(expected, rv.data)
        self.check_rank(self.rank2)

    def check_rank(self, rank):
        user = graph.find_node("User", self.user)
        node = graph.find_node("Value", self.node)
        assert user and node, "failed to find node and/or user"
        link = graph.find_link(user, node, "RANKS")
        assert link, "failed to find link"
        assert link.properties["rank"] == rank

    def check_status_code(self, code):
        assert code == 200, "status code not 200"

    def check_response(self, expected, data):
        response = json.loads(data)
        error = "expecting: {0}, actual: {1}".format(expected, response)
        assert response == expected, error


class GetNodeTests(unittest.TestCase):

    issue = "i1"
    value = "v1"
    objective = "o1"
    policy = "p1"

    def setUp(self):
        self.app = app.test_client()
        # create random user for testing
        self.user = "testuser-{0}".format(uuid.uuid4())
        user_data = dict(username=self.user, name="Test", city="Portland")
        graph.create_user(user_data)
    
    def get_runner(self, endpoint, node_id):
        data = dict(id=node_id)
        
        # submit GET request to retrieve node data
        rv = self.app.get(endpoint, data=data)
        
        # confirm JSON response contains input node_id
        response = json.loads(rv.data)
        contains_id = set(data.items()).issubset(set(response.items()))
        assert contains_id, "response does not contain node id"
        return response

    def test_get_issue(self):
        self.get_runner("/api/issue", self.issue)
    
    def test_get_value(self):
        self.get_runner("/api/value", self.value)
     
    def test_get_policy(self):
        self.get_runner("/api/policy", self.policy)
  
    def test_get_objective(self):
        self.get_runner("/api/objective", self.objective)

    def tearDown(self):
        # cleanup testuser
        graph.delete_user(self.user)


if __name__ == '__main__':
    unittest.main()



