from App import app
from webob import Request,Response
from App.service.book_service import BookService
from mahi_wsgi_web_framework.models import JSONResponse,HTMLResponse
service=BookService()

@app.route('/books/all',allowed_methods=["GET"])
def get_all_books(request:Request)->Response:
    # return JSONResponse(service.get_all())
    books:list[dict]=service.get_all()
    html_content=app.template("books.html",{"books":books})
    return HTMLResponse(html_content)


@app.route('/books',allowed_methods=["POST"])
def create_book(request:Request)->Response:
    book_created=service.create(request.json)
    return JSONResponse(book_created)

@app.route('/books/{book_id:d}',allowed_methods=["DELETE"])
def delete_book(request:Request,book_id:int)->Response:
    service.delete(book_id)
    return JSONResponse({
        "message":f"Book associated with {book_id} was deleted"
    })


