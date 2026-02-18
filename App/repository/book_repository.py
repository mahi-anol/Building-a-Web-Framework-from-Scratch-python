from App.models.book import Book
class BookRepository:

    def __init__(self):
        self._id=0
        self._books:list[Book]=[]
   
    def create(self,**kwargs)->Book:
        self._id+=1

        kwargs["id"]=self._id
        book=Book(**kwargs)
        self._books.append(book)
        return book._asdict()
    # def create(self,name:str,author:str)->Book:
    #     self._id=1
    #     # kwargs['id']=self._id
    #     book=Book(id=self._id,name=name,author=author)
    #     self._books.append(book)
    #     return book._as_dict()
    
    def all(self)->list[dict]:
        return [book._asdict() for book in self._books]
    
    def delete(self,id):
        for ind,book in enumerate(self._books):
            if book.id ==id:
                del self._books[ind]
                return True
        return False
    

