from helpers import json_response
from contants import inventory
from app import app

@app.route('/api/mobile')
def get_products(environ,start_response):
    return json_response(inventory['mobile'],start_response)

@app.route('/api/laptop')
def get_products(environ,start_response):
    return json_response(inventory['laptop'],start_response)
