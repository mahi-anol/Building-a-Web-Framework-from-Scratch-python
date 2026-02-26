from demo_app.models.book import Book
from demo_app import db

class BookRepository:  
   
    def create(self,instance:Book)->Book:
        db.save(instance)
        return instance
    def all(self)->list[dict]:
        return db.get_all(Book)
    
    def get_by_id(self,id:int)->Book|None:
        return db.get_by_id(Book,id)
    
    def delete(self,id):
        book_to_delete=self.get_by_id(id)
        db.delete(Book,book_to_delete.id)
    

