import sys
from os.path import dirname, abspath
import unittest

# add parent directory to path to allow importing app
root = dirname(dirname(dirname(abspath(__file__))))
sys.path.append(root)

from app import app, graph


class CypherRawTest(unittest.TestCase):
           
    def test_basic(self):
        cypher = graph.graph.cypher
        query = """
            MATCH (u:User)-[r:RANKS]-(v:Value)
            RETURN
                u.node_id AS username,
                r.rank AS rank,
                v.name AS name;
        """
        results = cypher.execute(query)
        for row in results:
            print row.username, row.rank, row.name


if __name__ == '__main__':
    unittest.main()
