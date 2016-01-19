import six
import os
import json
import unittest
import sys

# add parent directory to path to import app
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

from app import app, graph


def safe_data(data):
    # Helper for py2/py3 compatible string handling
    if isinstance(data, six.string_types):
        return json.loads(data)
    else:
        return json.loads(data.decode('utf-8'))


class IndexTests(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
    
    def test_index(self):
        rv = self.app.get('/')
        expected = "ROOT API"
        response = safe_data(rv.data)
        self.assertEqual(response, expected)

    def test_api_index(self):
        rv = self.app.get('/api') 
        expected = dict(response="API Index")
        response = safe_data(rv.data)
        self.assertEqual(response, expected)


if __name__ == '__main__':
    unittest.main()
