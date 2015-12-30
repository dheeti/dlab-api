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
        node = graph.find_node(node_type, args["id"])
        if node:
            return jsonify(
                name=node.properties["name"],
                id=node.properties["node_id"]
            )
        return jsonify(error="No matching node: {0}".format(args["id"]))

    @staticmethod
    def _get_user(args):
        # lookup user node and build json response
        node = graph.find_node("User", args["id"])
        if node:
            return jsonify(
                id=node.properties["node_id"],
                name=node.properties["name"],
                city=node.properties["city"]
            )
        return jsonify(error="No matching user: {0}".format(args["id"]))

    @staticmethod
    def post_rank(args, node_type):
        # apply ranking to node and return success status
        success, error = graph.rank(args, node_type)
        if success:
            return jsonify(success=success)
        return jsonify(success=success, error=error)

    @staticmethod
    def post_user(args):
        # create new user if it does not already exist
        user = args["username"]
        node, new_user = graph.create_user(args)
        if new_user:
            return jsonify(
                success="User <{0}> created".format(user),
                node_id=user
            )
        else:
            return jsonify(
                error="User <{0}> already exists".format(user),
                node_id=user
            )
