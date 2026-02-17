from webob import Request,Response
from App import app
from mahi_wsgi_web_framework.constants import HttpStatus
from App.data import inventory
from App.service.product_service import ProductService
from mahi_wsgi_web_framework.models import JSONResponse
@app.route('/api/products')
class ProductCreateController:
    def __init__(self):
        self.service=ProductService()
    
    def get(self,request:Request)->Response:
        return Response(
            json_body=self.service.get_all_products()
        )
    #create
    def post(self,request:Request)->Response:
        products=self.service.create_new_product(
            request.json
        )
        return Response(
            json_body=products
        )

@app.route('/api/products/{id:d}')
class ProductModifyController:
    def __init__(self):
        self.service=ProductService()
    
    def _get_product_not_found_response(self,product_id:int)->Response:
        return Response(
            json_body={
                'message':f"No product found with id {product_id}"
            },
            status=HttpStatus.NOT_FOUND
        )

    def get(self,request:Request,id:int)->Response:
        product=self.service.get_product_by_id(id)
        if not product:
            return self._get_product_not_found_response(id)
        return Response(
            json_body=product
        )
    
    def delete(self,request:Request,id:int):
        try:
            products=self.service.delete_product_by_id(id)
            return Response(
                json_body=products
            )
        except Exception as e:
            return Response(
                json_body={"message":str(e)},
                status=HttpStatus.NOT_FOUND
            )
        
@app.route('/api/products/{category}',allowed_methods=["GET"])
def get_products_by_cat(request:Request,category:str)->Response:
    if category not in inventory:
        return Response(
            json_body={
                "message":f"{category} doesn't exist in the inventory",

            },
            status=HttpStatus.NOT_FOUND
        )
    return JSONResponse(inventory[category])

@app.route('/api/exception')
def raise_exception(request:Request):
    raise ValueError("This is a test exception")