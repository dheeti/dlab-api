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


class Exists(object):
    """
    these nodes must exist in the neo4j instance you are running tests against
    """
    ISSUE = "i1"
    VALUE = "v1"
    OBJECTIVE = "o1"
    POLICY = "p1"


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
    
    DEFAULT_RANK = 1

    def setUp(self):
        self.app = app.test_client()
        
        # test defaults
        self.default_endpoint = "/api/value/rank"
        self.node_type = "Value"
        self.node = Exists.VALUE

        # make sure user exists
        self.user = "testuser-{0}".format(uuid.uuid4())
        self.user_data = dict(username=self.user, name="Test", city="Portland")
        graph.create_user(self.user_data)
        self.data = dict(
            user_id=self.user,
            rank=self.DEFAULT_RANK,
            issue_id=Exists.ISSUE
        )

    def tearDown(self):
        user = graph.find_node("User", self.user)
        node = graph.find_node(self.node_type, self.node)
        graph.delete_link(user, node, "RANKS")
        graph.delete_user(self.user)

    def valid_rank_runner(self, node_type, node):
        endpoint = os.path.join("/api", node_type.lower(), "rank")
        data = dict(self.data)
        self.node_type = node_type
        self.node = data["node_id"] = node
        rv = self.app.post(endpoint, data=data)
        expected = dict(success=True)
        self.check_status_code(rv.status_code)
        self.check_response(expected, rv.data)
        self.check_rank(self.DEFAULT_RANK)

    def test_rank_issue(self):
        self.data = dict(
            user_id=self.user,
            rank=self.DEFAULT_RANK
        )
        self.valid_rank_runner("Issue", Exists.ISSUE)

    def test_rank_value(self):
        self.valid_rank_runner("Value", Exists.VALUE)
    
    def test_rank_objective(self):
        self.valid_rank_runner("Objective", Exists.OBJECTIVE)
    
    def test_rank_policy(self):
        self.valid_rank_runner("Policy", Exists.POLICY)

    def test_invalid_rank_no_user(self):
        data = dict(self.data)
        data["user_id"] = uuid.uuid4()
        data["node_id"] = self.node 
        rv = self.app.post(self.default_endpoint, data=data)
        expected = dict(success=False, error="invalid user_id")
        self.check_status_code(rv.status_code)
        self.check_response(expected, rv.data)

    def test_invalid_rank_no_node(self):
        # invalid rank request, node does not exist
        data = dict(self.data)
        data["user_id"] = self.user
        data["node_id"] = uuid.uuid4()
        rv = self.app.post(self.default_endpoint, data=data)
        expected = dict(success=False, error="invalid node_id")
        self.check_status_code(rv.status_code)
        self.check_response(expected, rv.data)
    
    def test_update_rank(self):
        # rank a node then update the ranking
        data = dict(self.data)
        data["user_id"] = self.user
        data["node_id"] = self.node
        
        # rank node initially
        rv = self.app.post(self.default_endpoint, data=data)
        self.check_status_code(rv.status_code)
        expected = dict(success=True)
        self.check_response(expected, rv.data)
        self.check_rank(self.DEFAULT_RANK)

        new_rank = self.DEFAULT_RANK + 1

        # update rank
        data["rank"] = new_rank
        rv = self.app.post(self.default_endpoint, data=data)
        self.check_status_code(rv.status_code)
        expected = dict(success=True)
        self.check_response(expected, rv.data)
        self.check_rank(new_rank)

    def check_rank(self, rank):
        user = graph.find_node("User", self.user)
        node = graph.find_node(self.node_type, self.node)
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
        self.get_runner("/api/issue", Exists.ISSUE)
    
    def test_get_value(self):
        self.get_runner("/api/value", Exists.VALUE)
  
    def test_get_objective(self):
        self.get_runner("/api/objective", Exists.OBJECTIVE)
    
    def test_get_policy(self):
        self.get_runner("/api/policy", Exists.POLICY)

    def tearDown(self):
        # cleanup testuser
        graph.delete_user(self.user)


if __name__ == '__main__':
    unittest.main()
