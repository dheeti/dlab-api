import os

from flask import jsonify
from app import graph


class Handler(object):
    """
    dlab-api endpoint handlers
    """

    @staticmethod
    def index():
        return jsonify(response="API Index")

    @staticmethod
    def get_node(args, node_type):
        # use different handler if fetching a user
        if node_type == "User": return Handler._get_user(args)
       
        # lookup node and build json response
        node = graph.nodes.find(node_type, args["id"])
        if node:
            return jsonify(
                name=node.properties["name"],
                id=node.properties["node_id"]
            )
        return jsonify(error="No matching node: {0}".format(args["id"]))

    @staticmethod
    def _get_user(args):
        # lookup user node and build json response
        node = graph.nodes.find("User", args["id"])
        if node:
            return jsonify(
                id=node.properties["node_id"],
                name=node.properties["name"],
                city=node.properties["city"]
            )
        return jsonify(error="No matching user: {0}".format(args["id"]))

    @staticmethod
    def get_nodes(child_type, parent_type, args):
        kwargs = {}
        if parent_type:
            kwargs = dict(parent_label=parent_type, parent_id=args["filter_id"])
        data = graph.nodes.find_all(child_type, **kwargs)
        return jsonify(nodes=data)

    @staticmethod
    def post_rank(args, node_type):
        # apply ranking to node and return success status
        success, error = graph.user_rank(args, node_type)
        if success:
            return jsonify(success=success)
        return jsonify(success=success, error=error)

    @staticmethod
    def post_user(args):
        # create new user if it does not already exist
        user = args["username"]
        node, new_user = graph.create_user(args)
        if new_user:
            return jsonify(success=True, error="")
        else:
            error="User <{0}> already exists".format(user)
            return jsonify(success=False, error=error)
    
    @staticmethod
    def post_map(args, src_node, dst_node):
        success, error = graph.user_map(args, src_node, dst_node)
        return jsonify(success=success, error=error)
