from webob.response import Response
from tests.constants import BASE_URL
import pytest
from Framework.command_handlers import CommonHandlers
from Framework.exceptions import MethodNotAllowed
from Framework.middlewares import ErrorHandlerMiddleware
from Framework.models import TextResponse,JSONResponse
from Framework.constants import ContentType
from dataclasses import dataclass
def test_client_can_send_request(app,client):
    RESPONSE_TEXT="Hello from test client"
    @app.route("/test")
    def test_handler(req):
        return TextResponse(RESPONSE_TEXT)
    
    response=client.get(f"{BASE_URL}/test")
    assert response.text==RESPONSE_TEXT
    assert 'text/plain' in response.headers['Content-Type']


@pytest.mark.parametrize(
    "name, exp_result",
    [
        pytest.param(
            'Mahi',{"username":"Mahi"},id="Mahi"
        ),
        pytest.param(
            'Nafsi',{"username":"Nafsi"},id="Nafsi"
        )
    ]
)
def test_json_response_from_dict_based_data(app,client,name,exp_result):
    @app.route('/hello/{name}')
    def hello(req,name:str):
        return JSONResponse({"username":name})
    # Test multiple parameter values
    response:Response=client.get(f"{BASE_URL}/hello/{name}")
    assert response.json()==exp_result
    assert ContentType.JSON in response.headers["Content-Type"]

@pytest.mark.parametrize(
    "name, exp_result",
    [
        pytest.param(
            'Mahi',{"username":"Mahi"},id="Mahi"
        ),
        pytest.param(
            'Nafsi',{"username":"Nafsi"},id="Nafsi"
        )
    ]
)
def test_json_response_from_class_based_data(app,client,name,exp_result):
    @dataclass
    class Person:
        username:str
    @app.route('/hello/{name}')
    def hello(req,name:str):
        person=Person(name)
        return JSONResponse(person)
    # Test multiple parameter values
    response:Response=client.get(f"{BASE_URL}/hello/{name}")
    assert response.json()==exp_result
    assert ContentType.JSON in response.headers["Content-Type"]


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

def test_allowed_methods_for_fn_based_handler_without_middlewar(app,client):
    @app.route("/home",allowed_methods=["POST"])
    def home(req):
        return Response("Hello")
    
    with pytest.raises(MethodNotAllowed):
        client.get(f"{BASE_URL}/home")
    
    assert client.post(f"{BASE_URL}/home").text=="Hello"

def test_allowed_methods_for_fn_based_handler_with_middlewar(app,client):
    @app.route("/home",allowed_methods=["POST"])
    def home(req):
        return Response("Hello")
    
    app.add_middleware(ErrorHandlerMiddleware)
    
    get_response=client.get(f"{BASE_URL}/home")
    assert get_response.json()['message']==f'GET request is not allowed for /home'
    assert get_response.status_code==405

    post_response=client.post(f"{BASE_URL}/home")
    assert post_response.text=="Hello"
    assert post_response.status_code==200
## mod 1
# def test_parameterized_route(app,client):
#     @app.route('/hello/{name}')
#     def hello(req,name:str):
#         return Response(text=f"Hello {name}")
#     # Test multiple parameter values
#     assert client.get(f"{BASE_URL}/hello/Mahi").text=="Hello Mahi"
#     assert client.get(f"{BASE_URL}/hello/Nafsi").text=="Hello Nafsi"
