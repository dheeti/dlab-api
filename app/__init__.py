import os, sys

from flask import Flask
from flask.ext.cors import CORS
from graph import Graph


app = Flask(__name__)
app.config.from_object('config')
app.debug = True

CORS(app)

# check if neo4j uri has been set as environment variable
# otherwise use uri from config file
neo_uri = os.getenv("NEO4J_URI", "")
if not neo_uri: neo_uri = app.config["NEO4J_URI"]
graph = Graph(neo_uri)

from app.utils import crossdomain

from app import views
from app.mod_api.views import mod_api as api_module
app.register_blueprint(api_module)
