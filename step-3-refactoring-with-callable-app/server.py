from wsgiref.simple_server import make_server
from common_handlers import Handlers
from app import middleware
if __name__=="__main__":
    host="localhost"
    port=8000
    with make_server(host,port,middleware) as server:
        print(f"Listening to http://{host}:{port}")
        server.serve_forever()

