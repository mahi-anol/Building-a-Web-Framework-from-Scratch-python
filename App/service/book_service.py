from App.repository.book_repository import BookRepository
from App.exceptions import ResourceNotFoundException
class BookService:
    def __init__(self):
        self.repository=BookRepository()
        self.seed_data()
    def seed_data(self):
        self.repository.create(name="The Great Gatsby",author="F. Scott Fitzgerald")
        self.repository.create(name="Life of Pi",author="Yann Martal")

    def get_all(self):
        return self.repository.all()
    
    def create(self,request_body:dict)->dict:
        return self.repository.create(**request_body)
    
    def delete(self,book_id:int)->None:
        is_success=self.repository.delete(book_id)
        if not is_success:
            raise ResourceNotFoundException(f"Book associated with id: {book_id} not found")