from webob.response import Response
from tests.constants import BASE_URL
import pytest
from Framework.command_handlers import CommonHandlers
def test_client_can_send_request(app,client):
    RESPONSE_TEXT="Hello from test client"
    @app.route("/test")
    def test_handler(req):
        return Response(text=RESPONSE_TEXT)
    
    response=client.get(f"{BASE_URL}/test")
    assert response.text==RESPONSE_TEXT


@pytest.mark.parametrize(
    "name, exp_result",
    [
        pytest.param(
            'Mahi',"Hello Mahi",id="Mahi"
        ),
        pytest.param(
            'Nafsi',"Hello Nafsi",id="Nafsi"
        )
    ]
)
def test_parameterized_route(app,client,name,exp_result):
    @app.route('/hello/{name}')
    def hello(req,name:str):
        return Response(text=f"Hello {name}")
    # Test multiple parameter values
    assert client.get(f"{BASE_URL}/hello/{name}").text==exp_result


def test_url_not_found(app,client):
    RESPONSE_TEXT="Hello from test client"
    @app.route("/test")
    def test_handler(req):
        return Response(text=RESPONSE_TEXT)

    wrong_path="/hello"
    exp_response={
        "message":f"Request Path: {wrong_path} does not exist"
    }
    response=client.get(f"{BASE_URL}{wrong_path}")
    assert response.status_code==404
    assert response.json()==exp_response

def test_generic_exception_handler(app,client):
    msg="This is a test exception"
    exp_response={"message":f"Unhandled Exception Occured: {msg}"}
    app.add_exception_handler(CommonHandlers.generic_exception_handler)
    @app.route("/test")
    def test_handler(req):
        raise RuntimeError(msg)
    
    response=client.get(f"{BASE_URL}/test")
    assert response.status_code==500
    assert response.json()==exp_response
## mod 1
# def test_parameterized_route(app,client):
#     @app.route('/hello/{name}')
#     def hello(req,name:str):
#         return Response(text=f"Hello {name}")
#     # Test multiple parameter values
#     assert client.get(f"{BASE_URL}/hello/Mahi").text=="Hello Mahi"
#     assert client.get(f"{BASE_URL}/hello/Nafsi").text=="Hello Nafsi"
