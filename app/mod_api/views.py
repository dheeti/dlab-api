import os
from os.path import basename, dirname

from flask import Blueprint, request, jsonify, session
from webargs.flaskparser import use_args

from app import graph, crossdomain
from handlers import Handler
from auth import Authenticate
from args import Args

mod_api = Blueprint('api', __name__, url_prefix='/api')

"""
default error handler when request arguments do not match required arguments
as specified by use_args() input
"""
@mod_api.errorhandler(422)
def handle_bad_request(err):
    data = getattr(err, 'data')
    if data: message = data['exc'].messages
    else: message = "invalid request"
    return jsonify({"error": message }), 422


"""
api index
"""
@mod_api.route('/')
@crossdomain(origin="*")
def api_index():
    return Handler.index()


"""
create a new user
"""
@mod_api.route('/user', methods=["POST"])
@use_args(Args.post_user)
@crossdomain(origin="*")
def post_user(args):
    return Handler.post_user(args)


"""
login to create session cookie
"""
@mod_api.route('/login', methods=["POST"])
@use_args(Args.post_login)
@crossdomain(origin="*")
def login(args):
    success, error = Authenticate.login(graph, session, args)
    return jsonify(success=success, error=error)


"""
logout to remove session cookie
"""
@mod_api.route('/logout', methods=["POST"])
@use_args(Args.post_logout)
@crossdomain(origin="*")
def logout(args):
    success, error = Authenticate.logout(session)
    return jsonify(success=success, error=error)


"""
retrieve data about a node as specified by it's node_id
"""
@mod_api.route('/user', methods=['GET'])
@mod_api.route('/issue', methods=['GET'])
@mod_api.route('/value', methods=['GET'])
@mod_api.route('/objective', methods=['GET'])
@mod_api.route('/policy', methods=['GET'])
@use_args(Args.get_node)
@crossdomain(origin="*")
def get_node(args):
    node = basename(request.path).capitalize()
    return Handler.get_node(args, node) 


"""
retrieve data about a node as specified by it's node_id
"""
@mod_api.route('/community', methods=['GET'])
@use_args(Args.get_community)
@crossdomain(origin="*")
def get_community(args):
    node = basename(request.path).capitalize()
    if "id" in args:
        return Handler.get_node(args, node) 
    else:
        return Handler.get_nodes(node, None, args) 


"""
retrieve all nodes of a given type
"""
@mod_api.route('/community/issue', methods=['GET'])
@mod_api.route('/issue/value', methods=['GET'])
@mod_api.route('/issue/objective', methods=['GET'])
@mod_api.route('/issue/policy', methods=['GET'])
@use_args(Args.get_nodes)
@crossdomain(origin="*")
def get_nodes(args):
    parent = basename(dirname(request.path)).capitalize()
    child = basename(request.path).capitalize()
    return Handler.get_nodes(child, parent, args) 


"""
apply a ranking to a specific node as a user
"""
@mod_api.route('/rank/issue', methods=["POST"])
@mod_api.route('/rank/value', methods=["POST"])
@mod_api.route('/rank/objective', methods=["POST"])
@mod_api.route('/rank/policy', methods=["POST"])
@use_args(Args.post_rank)
@crossdomain(origin="*")
def post_rank(args):
    node = os.path.basename(request.path).capitalize()
    return Handler.post_rank(args, node)


"""
apply a mapping between nodes
Value -> Objective || Objective -> Policy
"""
@mod_api.route('/map/value/objective', methods=["POST"])
@mod_api.route('/map/objective/policy', methods=["POST"])
@use_args(Args.post_map)
@crossdomain(origin="*")
def post_map(args):
    src_node = os.path.basename(os.path.dirname(request.path)).capitalize()
    dst_node = os.path.basename(request.path).capitalize()
    return Handler.post_map(args, src_node, dst_node)
