from flask import Blueprint, request, jsonify

from app import app, crossdomain

@app.route('/')
def index():
    return "ROOT API"


@app.route('/login')
@crossdomain(origin="*")
def login():
    return "ROOT API"
