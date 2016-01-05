from flask import Blueprint, request, jsonify

from app import app, crossdomain

@app.route('/')
@crossdomain(origin="*")
def index():
    return "ROOT API"

@app.route('/login')
@crossdomain(origin="*")
def login():
    response = app.make_response("LOGIN")  
    response.set_cookie("test-cookie",value="1")
    return response
