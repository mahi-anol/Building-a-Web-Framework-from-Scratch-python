from contants import inventory
from app import app
from webob import Request,Response
from helpers import json_response
from contants import HttpStatus
from product_service import ProductService

@app.route('/api/products')
class ProductCreateController:
    def __init__(self):
        self.service=ProductService()
    def get(self,request:Request)->Response:
        return Response(
            json_body=self.service.get_all_products()
        )
    def post(self,request:Request)->Response:
        requested_product=request.json_body
        products=self.service.create_new_product(requested_product)
        return Response(
            json_body=products
        )
    
@app.route('/api/products/{id:d}')
class ProductModifyController:
    def __init__(self):
        self.service=ProductService()

    def get_product_not_found_response(self,product_id)->Response:
        return Response(
            json_body={"message":f"No product found with id {product_id}."},status=HttpStatus.NOT_FOUND
        )
    
    def get(self,request:Request,id:int)->Response:
        p=self.service._get_product_by_id(id)
        if not p:
            return self.get_product_not_found_response(id)
        return Response(json_body=p)
                            
    # def put(self,id:int):
    #     pass
    # def patch(self,id:int):
    #     pass
    def delete(self,request:Request,id:int):
        p=self.service._get_product_by_id(id)
        if not p:
            return self.get_product_not_found_response(id)
        products=self.service.delete_product(p)
        return Response(json_body=products)




# @app.route('/api/products')
# def get_products(request:Request):
#     return Response(json_body=inventory)

@app.route('/api/products/{category}')
def get_products(request:Request,category:str)->Response:
    if category not in inventory:
        return Response(json_body={"message":f"{category} does not exist."},status=HttpStatus.NOT_FOUND)
    return Response(json_body=inventory[category])
