from helpers import json_response
from middlewares import ErrorHandlerMiddleware
from common_handlers import Handlers
inventory={

    "mobile":[
        {
            "product_id":1,"product_name":"S25 ultra","brand":"Samsung"
        },
        {
            "product_id":2,"product_name":"iphone","brand":"Apple"
        }
    ],
    "laptop":[
        {
            "product_id":3,"product_name":"Macbook Pro M4","brand":"Apple"
        },
        {
            "product_id":4,"product_name":"Dell XPS","brand":"Dell"
        }
    ]
}


class Application:
    def __init__(self):
        pass
    def __call__(self,environ,start_response,*args,**kwargs):
        path=environ.get("PATH_INFO","/")
        category=path.split("/")[-1]

        products=inventory.get(category,[])
        # raise RuntimeError("Just a test exception")
        return json_response(products,start_response)

app=Application()
middleware=ErrorHandlerMiddleware(
    app=app,ExceptionHandler=Handlers.generic_exception_handler
)