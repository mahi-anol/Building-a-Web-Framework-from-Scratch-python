from wsgiref.simple_server import make_server


class HttpStatus:
    OK="200 OK"

class ContentType:
    TEXT=('Content-type','text/plain')



def my_application(environ,start_response):
    print("In my application")
    # response_body=[
    #     f'{key}: {value}' for key,value in sorted(environ.items())
    # ]

    path=environ.get("PATH_INFO ","/")
    response_body=f"Responding from my application PATH: {path}" 



    response_text="\n".join(response_body)
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