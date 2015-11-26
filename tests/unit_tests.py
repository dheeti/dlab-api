import os
import json
import unittest
import sys

api_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(api_dir)

from app import app

 
class BasicTest(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
 
    def test_index(self):
        rv = self.app.get('/api')
        expected = dict(response="API Index")
        response = json.loads(rv.data)
        self.assertEqual(response, expected)


if __name__ == '__main__':
    unittest.main()
