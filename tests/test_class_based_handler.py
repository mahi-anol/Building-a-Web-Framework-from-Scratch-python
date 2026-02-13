from webob import Response

def test_class_based_handler_get(app,client):
    response_text="This is a {} request"
    @app.route("/books")
    class BookResource:
        def get(self,req):
            return Response(response_text.format("GET"))
        def post(self,req):
            return Response(response_text.format("POST"))
        

    response=client.get('http://testserver/books')
    assert response.text==response_text.format("GET")

    response=client.post('http://testserver/books')
    assert response.text==response_text.format("POST")


def test_class_based_handler_method_not_allowed(app,client):
    exp_response={"message":"{} request is not allowed for /books"}

    @app.route("/books")
    class BookResource:
        def get(self,req):
            return Response("This is a get request")

    response=client.post("http://testserver/books")
    assert response.status_code==405
    assert response.json()['message']==exp_response["message"].format('POST')
# mod 1
# def test_class_based_handler_get(app,client):
#     response_text="This is a GET request"
#     @app.route("/books")
#     class BookResource:
#         def get(self,req):
#             return Response(response_text)
    
#     response=client.get('http://testserver/books')
#     assert response.text==response_text