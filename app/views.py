from flask import Blueprint, request, jsonify

from app import app, crossdomain

@app.route('/')
@crossdomain(origin="*")
def index():
    return "ROOT API"
