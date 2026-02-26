from demo_app.repository.book_repository import BookRepository
from mahi_wsgi_web_framework.orm.exeptions import RecordNotFound
from demo_app.models.book import Book
from demo_app.exceptions import ResourceNotFoundException
class BookService:
    def __init__(self):
        self.repository=BookRepository()
        self.seed_data()
    def seed_data(self):
        books:list[Book]=self.repository.all()
        if not books:
            self.repository.create(Book(name="The Great Gatsby",author="F. Scott Fitzgerald"))
            self.repository.create(Book(name="Life of Pi",author="Yann Martal"))

    def get_all(self):
        return self.repository.all()
    
    def create(self,request_body:dict)->dict:

        return self.repository.create(
            instance=Book(**request_body)
        )
    
    def delete(self,book_id:int)->None:
        try:
            self.repository.delete(book_id)
        except RecordNotFound:
            raise ResourceNotFoundException(f"Book associated with id: {book_id} not found")