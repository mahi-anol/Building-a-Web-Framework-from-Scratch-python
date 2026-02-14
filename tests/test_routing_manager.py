import pytest
# from Framework import wsgi_framework
from webob import Response
from tests.conftest import TFramework
from tests.constants import BASE_URL


def test_basic_route_adding(app:TFramework):
    @app.route("/home")
    def home(req):
        return Response(
            text="Hello World"
        )
    
def test_duplicate_routing_exception(app:TFramework):
    @app.route("/test")
    def first(req):
        return Response(
            text="First Handler"
        )
    with pytest.raises(RuntimeError,match=f"Path: /test already bind to another handler."):
        @app.route("/test")
        def second(req):
            return Response(
                text="First Handler"
            )

def test_explicitly_registered_route(app,client):
    RESPONSE_TEXT="Hello from test client"
    
    def test_handler(req):
        return Response(text=RESPONSE_TEXT)
    
    app.add_route("/test",test_handler)

    response=client.get(f"{BASE_URL}/test")
    assert response.text==RESPONSE_TEXT

## mod-1
# @pytest.fixture
# def app()->wsgi_framework:
#     return wsgi_framework()

# def test_basic_route_adding(app:wsgi_framework):
#     @app.route("/home")
#     def home(req):
#         return Response(
#             text="Hello World"
#         )
    
# def test_duplicate_routing_exception(app:wsgi_framework):
#     @app.route("/test")
#     def first(req):
#         return Response(
#             text="First Handler"
#         )
#     with pytest.raises(RuntimeError,match=f"Path: /test already bind to another handler."):
#         @app.route("/test")
#         def second(req):
#             return Response(
#                 text="First Handler"
#             )