from flask import Blueprint, request

from app import app, crossdomain

@app.route('/')
@crossdomain(origin="*")
def index():
    return "ROOT API"
