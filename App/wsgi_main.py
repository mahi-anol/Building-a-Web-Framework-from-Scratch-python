from wsgiref.simple_server import make_server
from App import exception_handler_middleware as app
from App.api import product_controller
from App.view import home_controller
if __name__=="__main__":
    host="localhost"
    port=8000

    with make_server(host=host,port=port,app=app) as server:
        print(f"Listening to http://{host}:{port}")
        server.serve_forever()  