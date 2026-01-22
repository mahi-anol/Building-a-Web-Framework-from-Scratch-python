from wsgiref.simple_server import make_server,demo_app
import json

class HttpStatus:
    OK="200 OK"
    INTERNAL_SERVER_ERROR="500 Internal Server Error"

class JsonContentType:
    type=('content-type','text/json')

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

def json_response(response: dict | list[dict],start_response,status=HttpStatus.OK,response_headers=[]):
    response_body=json.dumps(response)
    response_headers.append(JsonContentType.type)
    start_response(status,response_headers)
    return [response_body.encode("utf-8")]

class Handlers:
    @staticmethod
    def generic_exception_handler(environ,start_response,ex:Exception)->list[bytes]:
        response={
            "message": f" Unhandled exception occured {str(ex)}"
        }
        return json_response(
            response=response,
            start_response=start_response,
            status=HttpStatus.INTERNAL_SERVER_ERROR
        )
class ErrorHandlerMiddleware:
    def __init__(self,app,ExceptionHandler:callable ):
        self.wrapped_app=app
        self.ExceptionHandler=ExceptionHandler
    def __call__(self,envrion,start_response,*args,**kwds):
        try:
            return self.wrapped_app(envrion,start_response,*args,**kwds)
        except Exception as e:
            return self.ExceptionHandler(envrion,start_response,e)
           



def my_application(environ,start_response):

    path=environ.get("PATH_INFO","/")
    category=path.split("/")[-1]

    products=inventory.get(category,[])
    raise RuntimeError("Just a test exception")
    return json_response(products,start_response)
    



if __name__=="__main__":
    host="localhost"
    port=8000

    wrapped_app=ErrorHandlerMiddleware(app=my_application,ExceptionHandler=Handlers.generic_exception_handler)
    server=make_server(host=host,port=port,app=wrapped_app)
    print(f"Listening to http://{host}:{port}")
    server.serve_forever()
    