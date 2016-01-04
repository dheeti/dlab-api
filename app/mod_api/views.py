import os

from flask import Blueprint, request, jsonify
from webargs.flaskparser import use_args

from app import graph
from handlers import Handler
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


@mod_api.route('/')
def api_index():
    return Handler.index()


"""
retrieve data about a node as specified by it's node_id
"""
@mod_api.route('/user', methods=['GET'])
@mod_api.route('/community', methods=['GET'])
@mod_api.route('/issue', methods=['GET'])
@mod_api.route('/value', methods=['GET'])
@mod_api.route('/objective', methods=['GET'])
@mod_api.route('/policy', methods=['GET'])
@use_args(Args.get_node)
def get_node(args):
    node = os.path.basename(request.path).capitalize()
    return Handler.get_node(args, node) 


"""
apply a ranking to a specific node as a user
"""
@mod_api.route('/rank/issue', methods=["POST"])
@mod_api.route('/rank/value', methods=["POST"])
@mod_api.route('/rank/objective', methods=["POST"])
@mod_api.route('/rank/policy', methods=["POST"])
@use_args(Args.post_rank)
def post_rank(args):
    node = os.path.basename(request.path).capitalize()
    return Handler.post_rank(args, node)


"""
create a new user
"""
@mod_api.route('/user', methods=["POST"])
@use_args(Args.post_user)
def post_user(args):
    return Handler.post_user(args)


"""
apply a mapping between nodes
Value -> Objective || Objective -> Policy
"""
@mod_api.route('/map/value/objective', methods=["POST"])
@mod_api.route('/map/objective/policy', methods=["POST"])
@use_args(Args.post_map)
def post_map(args):
    src_node = os.path.basename(os.path.dirname(request.path)).capitalize()
    dst_node = os.path.basename(request.path).capitalize()
    return Handler.post_map(args, src_node, dst_node)
