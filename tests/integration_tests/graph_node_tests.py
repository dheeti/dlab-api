import sys
from os.path import dirname, abspath
import unittest

import py2neo

# add parent directory to path to allow importing app
root = dirname(dirname(dirname(abspath(__file__))))
sys.path.append(root)

from app import graph
from shared.neo_utils import Handler, Node, Link


class NodesFindAllTest(unittest.TestCase):

    def setUp(self):
        self.handler = Handler()
        self.issue = Node(self.handler, "TestIssue")
        self.nodes = [ Node(self.handler, "TestValue") for i in range(0, 3) ]        
        Link(self.handler, self.issue.node, self.nodes[0].node, "HAS") 
        Link(self.handler, self.issue.node, self.nodes[1].node, "HAS") 

    def tearDown(self):
        self.handler.clean_up()

    def test_findall(self):
        """
        test that all TestValue nodes are returned
        """
        node_ids = [ node.node_id for node in self.nodes ]
        nodes = graph.nodes.find_all("TestValue")
        for node in nodes:
            self.assertIn(node["node_id"], node_ids)

    def test_parent_issue_findall(self):
        """
        test that only first two TestValue nodes are returned as the last node does
        not have a link from the TestIssue node
        """
        node_ids = [self.nodes[0].node_id, self.nodes[1].node_id]
        args = dict(parent_id=self.issue.node_id, parent_label="TestIssue")
        nodes = graph.nodes.find_all("TestValue", **args)
        for node in nodes:
            self.assertIn(node["node_id"], node_ids)
            self.assertNotEqual(node["node_id"], self.nodes[2].node_id)


if __name__ == '__main__':
    unittest.main()
