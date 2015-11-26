from flask import Blueprint, request, jsonify
from webargs import fields
from webargs.flaskparser import use_args

from app import app


mod_api = Blueprint('api', __name__, url_prefix='/api')

@mod_api.errorhandler(422)
def handle_bad_request(err):
    data = getattr(err, 'data')
    if data: message = data['exc'].messages
    else: message = "invalid request"
    return jsonify({"error": message }), 422


@mod_api.route('/')
def api_index():
    return jsonify(response="API Index")


entity_args = {
    'id':fields.Str(required=True),
}

def get_entity_response(entity_id, name, desc):
    return dict(id=entity_id, name=name, desc=desc)

@mod_api.route('/value', methods=['GET'])
@use_args(entity_args)
def get_value(args):
    value_id = args["id"]
    response = get_entity_response(value_id, "Fairness", "We can share")
    return jsonify(response)


