from wsgiref.simple_server import make_server
from demo_app import app
from demo_app.api import product_controller,auth_controller
from demo_app.view import home_controller,book_controller
if __name__=="__main__":
    host="localhost"
    port=8000
    with make_server(host=host,port=port,app=app) as server:
        print(f"Listening to http://{host}:{port}")
        server.serve_forever()  