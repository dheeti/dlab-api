from py2neo import Graph as NeoGraph, Node, Relationship


class Graph(object):

    def __init__(self, neo4j_uri):
        self.graph = NeoGraph(neo4j_uri)

    def find_node(self, label, node_id):
        args = dict(property_key="node_id", property_value=node_id)
        return self.graph.find_one(label, **args)

    def find_link(self, start_node, end_node, rel_type):
        args = dict(start_node=start_node, end_node=end_node, rel_type=rel_type)
        return self.graph.match_one(**args)

    def create_user(self, args):
        node = self.find_node("User", args["username"])
        if not node:
            properties = dict(
                node_id=args["username"],
                name=args["name"],
                city=args["city"]
            )
            node = Node("User", **properties)
            self.graph.create(node)
            return node, True
        return node, False

    def delete_user(self, user):
        node = self.find_node("User", user)
        if node:
            self.graph.delete(node)    
            return True
        return False
    
    def delete_link(self, start, end, link_type):
        if start and end:
            link = self.find_link(start, end, link_type)
            if link:
                self.graph.delete(link)
                return True
        return False

    def rank(self, args, node_type):
        success = False
        errors = []

        user = self.find_node("User", args["user_id"])
        if not user: return False, "invalid user_id"
      
        node = self.find_node(node_type, args["node_id"])
        if not node: return False, "invalid node_id"
        
        link = self.find_link(user, node, "RANKS")
        if link and ("issue_id" not in args or
                link.properties["issue_id"] == args["issue_id"]):
            link.properties["rank"] = args["rank"]
            link.push()
        else:
            properties = {
                "user_id":args["user_id"],
                "rank":args["rank"]
            }
            if "issue_id" in args: properties["issue_id"] = args["issue_id"]
            self.graph.create(Relationship(user, "RANKS", node, **properties))
        return True, "" 
