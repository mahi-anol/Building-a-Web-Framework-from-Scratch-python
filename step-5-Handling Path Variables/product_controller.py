from contants import inventory
from app import app
from webob import Request,Response
from helpers import json_response
from contants import HttpStatus
@app.route('/api/products')
def get_products(request:Request):
    return Response(json_body=inventory)

@app.route('/api/products/{category}')
def get_products(request:Request,category:str)->Response:
    if category not in inventory:
        return Response(json_body={"message":f"{category} does not exist."},status=HttpStatus.NOT_FOUND)
    return Response(json_body=inventory[category])
