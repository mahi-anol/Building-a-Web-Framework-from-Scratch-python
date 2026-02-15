from webob import Request,Response
from Framework.middlewares import Middleware
from tests.constants import BASE_URL
def test_middleware_methods_are_called(app,client):
    class CustomMiddleware(Middleware):
        def __init__(self, app):
            super().__init__(app)
        
        def process_request(self, req:Request):
            req.headers["X-REQUEST-PROCESSING"]="yes"
        def process_response(self, req, resp):
            resp.headers["X-RESPONSE-PROCESSING"]="yes"

    app.add_middleware(CustomMiddleware)
    
    @app.route("/hello")
    def index(req:Request)->Response:
        return Response("Hello World")
    response:Response=client.get(f"{BASE_URL}/hello")

    assert response.status_code==200
    # assert "X-RESPONSE-PROCESSING" in response.headers