from contants import inventory,products
from app import app
from webob import Request,Response
from helpers import json_response
from contants import HttpStatus


@app.route('/api/products')
class ProductCreateController:
    def get(self,request:Request)->Response:
        return Response(
            json_body=products
        )
    def post(self,request:Request)->Response:
        requested_product=request.json_body
        products.append(requested_product)
        return Response(
            json_body=products
        )
    
@app.route('/api/products/{id:d}')
class ProductModifyController:

    def _get_product_by_id(self,product_id:int)->dict|None:
        for p in products:
            if p['id']==product_id:
                return p
        return None
    
    def get_product_not_found_response(self,product_id)->Response:
        return Response(
            json_body={"message":f"No product found with id {product_id}."},status=HttpStatus.NOT_FOUND
        )

    def get(self,request:Request,id:int)->Response:
        p=self._get_product_by_id(id)
        if not p:
            return self.get_product_not_found_response(id)
        return Response(json_body=p)
                            
    # def put(self,id:int):
    #     pass
    # def patch(self,id:int):
    #     pass
    def delete(self,request:Request,id:int):
        p=self._get_product_by_id(id)
        if not p:
            return self.get_product_not_found_response(id)
        products.remove(p)
        return Response(json_body=products)




# @app.route('/api/products')
# def get_products(request:Request):
#     return Response(json_body=inventory)

@app.route('/api/products/{category}')
def get_products(request:Request,category:str)->Response:
    if category not in inventory:
        return Response(json_body={"message":f"{category} does not exist."},status=HttpStatus.NOT_FOUND)
    return Response(json_body=inventory[category])
