from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from app.mod_api.views import mod_api as api_module

app.register_blueprint(api_module)

