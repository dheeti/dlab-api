from py2neo import Graph as NeoGraph, Node, Relationship

from mod_api.auth import Authenticate


class Nodes(object):

    def __init__(self, graph):
        self.graph = graph

    def find(self, label, node_id):
        args = dict(property_key="node_id", property_value=node_id)
        return self.graph.find_one(label, **args)
    
    def find_all(self, label, **kwargs):
        if "parent_label" in kwargs and "parent_id" in kwargs:
            parent = self.find(kwargs["parent_label"], kwargs["parent_id"])
            if parent:
                return [ link.end_node.properties for link in parent.match() ]
        else:
            return [ node.properties for node in self.graph.find(label) ]

    def create(self, node_type, properties):
        node = Node(node_type, **properties)
        self.graph.create(node)
        return node, True
    
    def delete(self, node_type, node_id):
        node = self.find(node_type, node_id)
        if node:
            self.graph.delete(node)    
            return True
        return False


class Links(object):
    
    def __init__(self, graph):
        self.graph = graph
   
    def find(self, start_node, end_node, rel_type):
        args = dict(start_node=start_node, end_node=end_node, rel_type=rel_type)
        return self.graph.match_one(**args)
       
    def create(self, src, dst, link_type, properties):
        link = self.find(src, dst, link_type)
        if not link:
            link = Relationship(src, link_type, dst, **properties)
            self.graph.create(link)
        return link
    
    def delete(self, start, end, link_type):
        if start and end:
            link = self.find(start, end, link_type)
            if link:
                self.graph.delete(link)
                return True
        return False


class Graph(object):

    def __init__(self, neo4j_uri):
        self.graph = NeoGraph(neo4j_uri)
        self.nodes = Nodes(self.graph)
        self.links = Links(self.graph)
    
    def create_user(self, args):
        node = self.nodes.find("User", args["username"])
        if not node:
            passhash = Authenticate.hashgen(args["username"], args["password"])
            properties = dict(
                node_id=args["username"],
                name=args["name"],
                city=args["city"],
                passhash=passhash
            )
            node = Node("User", **properties)
            self.graph.create(node)
            return node, True
        return node, False

    def user_rank(self, args, node_type):
        success = False
        errors = []

        user = self.nodes.find("User", args["user_id"])
        if not user: return False, "invalid user_id"
      
        node = self.nodes.find(node_type, args["node_id"])
        if not node: return False, "invalid node_id"
        
        link = self.links.find(user, node, "RANKS")
        if link and ("issue_id" not in args or
                link.properties["issue_id"] == args["issue_id"]):
            link.properties["rank"] = args["rank"]
            link.push()
        else:
            properties = {"rank":args["rank"]}
            if "issue_id" in args: properties["issue_id"] = args["issue_id"]
            self.graph.create(Relationship(user, "RANKS", node, **properties))
        
        return True, "" 
    
    def user_map(self, args, src_node, dst_node):
        # TODO refactor this into smaller units

        success = False
        errors = []

        # retrieve nodes and existing links
        user = self.nodes.find("User", args["user_id"])
        if not user: errors.append("invalid user_id")
        src = self.nodes.find(src_node, args["src_id"])
        if not src: errors.append("invalid src_id")
        dst = self.nodes.find(dst_node, args["dst_id"])
        if not dst: errors.append("invalid dst_id")
        src_link = self.links.find(user, src, "RANKS")
        if not src_link: errors.append("user has not ranked src_node")
        dst_link = self.links.find(user, dst, "RANKS")
        if not dst_link: errors.append("user has not ranked dst_node")
        if errors: return False, ", ".join(errors)
       
        src_rank = src_link.properties["rank"]
        dst_rank = dst_link.properties["rank"]

        # fetch map node or create if it doesn't exist
        map_id = "{0}-{1}".format(args["src_id"], args["dst_id"])
        map_node = self.nodes.find("Map", map_id) 
        if not map_node:
            properties = dict(node_id=map_id)
            map_node = Node("Map", **properties)
            self.graph.create(map_node)
            self.graph.create(Relationship(src, "MAPS", map_node, **{}))
            self.graph.create(Relationship(map_node, "MAPS", dst, **{}))
        
        user_map_link = self.links.find(user, map_node, "MAPS")
        if user_map_link:
            # link already exists, update strength
            user_map_link.properties["strength"] = args["strength"]
            user_map_link.properties["src_rank"] = src_rank
            user_map_link.properties["dst_rank"] = dst_rank
            self.graph.push()
        else:
            # create new link from user to map node
            properties = dict(
                strength=args["strength"],
                src_rank=src_rank,
                dst_rank=dst_rank
            )
            self.graph.create(Relationship(user, "MAPS", map_node, **properties))
        
        return True, ""

    def get_summary(self, issue_id, node_type):
        issue = self.nodes.find("Issue", issue_id) 
        if not issue:
            return False, "issue <{0}> does not exist".format(issue_id)
        
        # TODO only grab nodes that are connected to issue node
        cypher = self.graph.cypher
        query = """
            MATCH (u:User)-[r:RANKS]-(v:`{0}`)
            RETURN
                r.rank AS rank,
                v.node_id AS node_id,
                count(u.node_id) AS count
            ORDER BY
                node_id, rank
        """.format(node_type)
        results = cypher.execute(query)
        nodes = {}
        for row in results:
            if row.node_id not in nodes:
                nodes[row.node_id] = [0, 0, 0, 0, 0]
            nodes[row.node_id][row.rank + 2] = row.count
        return True, nodes
