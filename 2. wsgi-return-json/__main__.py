from wsgiref.simple_server import make_server,demo_app
import json

class HttpStatus:
    OK="200 OK"

class ContentType:
    TEXT=('content-type','text/json')

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

def my_application(environ,start_response):

    path=environ.get("PATH_INFO","/")
    category=path.split("/")[-1]

    products=inventory.get(category,[])
    response_body=json.dumps(products) 
    
    response_headers=[
        ContentType.TEXT 
    ]
    status=HttpStatus.OK

    start_response(status,response_headers)

    return [response_body.encode("utf-8")]


if __name__=="__main__":
    host="localhost"
    port=8000
    server=make_server(host=host,port=port,app=my_application)
    print(f"Listening to http://{host}:{port}")
    server.serve_forever()