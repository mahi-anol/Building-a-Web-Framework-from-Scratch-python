from wsgiref.simple_server import make_server,demo_app
import json

class HttpStatus:
    OK="200 OK"

class ContentType:
    TEXT=('content-type','text/json')



def my_application(environ,start_response):
    print("In my application")
    # response_body=[
    #     f'{key}: {value}' for key,value in sorted(environ.items())
    # ]

    path=environ.get("PATH_INFO ","/")
    # response_body=f"Responding from my application PATH: {path}" 

    data=[
        {"product_id": 1, "product_name":"samsung"},
        {"product_id": 2,"product_name":"iphone"}
    ]

    response_body=json.dumps(data)


    response_text=''.join(response_body)
    headers=[
        ContentType.TEXT 
    ]
    start_response(HttpStatus.OK,headers)
    return [response_text.encode("utf-8")]


if __name__=="__main__":
    host="localhost"
    port=8000
    server=make_server(host=host,port=port,app=my_application)
    print(f"Listening to http://{host}:{port}")
    server.serve_forever()