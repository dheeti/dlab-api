import sys
from os.path import dirname, abspath
import json
import unittest
import uuid

import py2neo

# add parent directory to path to allow importing app
root = dirname(dirname(dirname(abspath(__file__))))
sys.path.append(root)

from app import app, graph


class UserTest(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.user_id = "testuser-{0}".format(uuid.uuid4())
        self.endpoint = "/api/user"
        self.data = dict(username=self.user_id, name="Test", city="Portland")

    def tearDown(self):
        graph.nodes.delete("User", self.user_id)


class CreateNewUserTest(UserTest):

    def test(self):
        graph.nodes.delete("User", self.user_id)
        
        # submit POST request to create new user
        rv = self.app.post(self.endpoint, data=self.data)
        
        # confirm JSON response matches what we expect
        response = json.loads(rv.data)
        expected = dict(
            node_id=self.user_id,
            success="User <{0}> created".format(self.user_id)
        )
        self.assertEqual(response, expected)
        
        # query graph directly and verify node exists
        node = graph.nodes.find("User", self.user_id)
        self.assertIsNotNone(node, msg="User node is null")
        self.assertEqual(node.properties["node_id"], self.user_id)


class CreateExistingUserTest(UserTest):
        
    def test(self):
        graph.create_user(self.data)
        
        # submit POST request to create a user that already exists
        rv = self.app.post(self.endpoint, data=self.data)

        # confirm JSON response matches what we expect
        response = json.loads(rv.data)
        expected = dict(
            node_id=self.user_id,
            error="User <{0}> already exists".format(self.user_id)
        )
        self.assertEqual(response, expected)
       

class GetExistingUserTest(UserTest):

    def test(self):
        graph.create_user(self.data)

        # submit GET request to retrieve user data
        rv = self.app.get("/api/user", data=dict(id=self.user_id))
        
        # confirm JSON response matches what we expect
        response = json.loads(rv.data)
        expected = dict(
            id=self.data["username"],
            name=self.data["name"],
            city=self.data["city"]
        )
        self.assertEqual(response, expected)


if __name__ == '__main__':
    unittest.main()
