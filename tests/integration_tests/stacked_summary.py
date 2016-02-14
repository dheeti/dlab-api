import sys
import json
from os.path import dirname, abspath
import unittest

# add parent directory to path to allow importing app
root = dirname(dirname(dirname(abspath(__file__))))
sys.path.append(root)


from app import app, graph


class GetSummaryTests(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.endpoint = "/api/summary/value"

    def parameters(self):
        return dict(
            issue_id="i1"
        )

    def check_status_code(self, code):
        assert code == 200, "status code not 200"

    def test_valid(self):
        rv = self.app.get(self.endpoint, data=self.parameters())
        self.check_status_code(rv.status_code)
        response = json.loads(rv.data)
        self.assertTrue(response["success"], msg="success not true")
        for key, value in response["data"].iteritems():
            self.assertIs(len(value["data"]), 5)


if __name__ == '__main__':
    unittest.main()
