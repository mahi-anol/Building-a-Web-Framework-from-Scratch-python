from webob import Request,Response
from mahi_wsgi_web_framework.middlewares import Middleware
from tests.constants import BASE_URL


def test_middleware_methods_are_called(app,client):
    class CustomMiddleware0(Middleware):
        def process_request(self, req:Request):
            assert "X-REQUEST-PROCESSING" not in req.headers
            req.headers["X-REQUEST-PROCESSING"]=0
        def process_response(self, req, resp):
            assert "X-RESPONSE-PROCESSING" in resp.headers
            assert resp.headers["X-RESPONSE-PROCESSING"]=="1"
            resp.headers["X-RESPONSE-PROCESSING"]=str(int(resp.headers["X-RESPONSE-PROCESSING"])+1)

    class CustomMiddleware1(Middleware):
        def process_request(self, req:Request):
            assert "X-REQUEST-PROCESSING" in req.headers
            assert req.headers["X-REQUEST-PROCESSING"]==0
            req.headers["X-REQUEST-PROCESSING"]=req.headers["X-REQUEST-PROCESSING"]+1
        def process_response(self, req, resp):
            assert "X-RESPONSE-PROCESSING" in resp.headers
            assert resp.headers["X-RESPONSE-PROCESSING"]=="0"
            resp.headers["X-RESPONSE-PROCESSING"]=str(int(resp.headers["X-RESPONSE-PROCESSING"])+1)

    class CustomMiddleware2(Middleware):
        def process_request(self, req:Request):
            assert "X-REQUEST-PROCESSING" in req.headers
            assert req.headers["X-REQUEST-PROCESSING"]==1
            req.headers["X-REQUEST-PROCESSING"]=req.headers["X-REQUEST-PROCESSING"]+1
        def process_response(self, req, resp):
            assert "X-RESPONSE-PROCESSING" not in resp.headers
            resp.headers["X-RESPONSE-PROCESSING"]= "0"

    app.add_middleware(CustomMiddleware2)    
    app.add_middleware(CustomMiddleware1)
    app.add_middleware(CustomMiddleware0)

    @app.route("/hello")
    def index(req:Request)->Response:
        assert "X-REQUEST-PROCESSING" in req.headers
        assert req.headers["X-REQUEST-PROCESSING"]==2
        return Response("Hello World")
    response:Response=client.get(f"{BASE_URL}/hello")

    assert response.status_code==200
    assert "X-RESPONSE-PROCESSING" in response.headers
    assert response.headers["X-RESPONSE-PROCESSING"]=="2"