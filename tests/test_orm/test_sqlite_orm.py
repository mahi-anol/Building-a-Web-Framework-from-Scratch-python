from mahi_wsgi_web_framework.orm.sqlite_orm import Database
from mahi_wsgi_web_framework.orm.exeptions import RecordNotFound
from tests.test_orm.conftest import Author,Book
import sqlite3
import os
import pytest
from mahi_wsgi_web_framework.utils.json_utils import JSONUtils
class TestSqliteORM:

    def setup_class(self):
        self.db=Database("./test.db")

    def test_db_connection(self):
        assert isinstance(self.db.connection,sqlite3.Connection)
        # assert db.tables==[]

    def test_create_table(self):
        self.db.create(Author)
        self.db.create(Book)
        db_tables=self.db.tables
        # print(Author._get_create_sql())
        assert "author" in db_tables
        assert "book" in db_tables

    def test_define_tables(self):
        assert Author.name.type==str
        assert Author.name.sql_type=="TEXT"

        assert Book.author.table==Author
        assert Author.age.sql_type=="INTEGER"

    def test_table_creation_sql(self):
        assert Author._get_create_sql() == "CREATE TABLE IF NOT EXISTS author (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER);"
        assert Book._get_create_sql() == "CREATE TABLE IF NOT EXISTS book (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, published INTEGER, author_id INTEGER);"

    def test_row_insertion_query(self):
        author=Author(name="Author 1",age="25")
        book=Book(title="Test Book",published=1,author=author)

        aq,av=author._get_insert_sql()
        bq,bv=book._get_insert_sql()
        assert aq=='INSERT INTO author (id, name, age) VALUES (?, ?, ?);'
        assert bq=='INSERT INTO book (id, title, published, author_id) VALUES (?, ?, ?, ?);'

    
    def test_row_insertion(self):
        author=Author(name="Farry C.",age="45") # Row
        #insert author first
        self.db.save(author)
        assert author.id is not None
        assert author.name=="Farry C."
        assert author.age=="45"

        book=Book(title="The house of dragon",published=1,author=author)
        self.db.save(book)
        assert book.id is not None
        assert book.author == author

    def teardown_class(self):
        self.db.connection.close()
        os.remove("./test.db")


class TestSqliteORMRead:
    def setup_class(self):
        self.db=Database("./test.db")
        self.db.create(Author)
        self.db.create(Book)
    
    def test_get_all_sql(self):
        sql,fields=Author._get_select_all_sql()
        assert sql=="SELECT id, name, age FROM author;"
        assert fields==['id','name', 'age']

        sql,fields=Book._get_select_all_sql()
        assert sql=="SELECT id, title, published, author_id FROM book;"
        assert fields==['id','title', 'published',"author_id"]


    def test_get_all(self):
        author=Author(name="Garry C.",age=45)
        self.db.save(author)
        book=Book(title="The house of dragon",published=True,author=author)
        self.db.save(book)

        author=Author(name="Kathy Sierra",age=60)
        self.db.save(author)
        book=Book(title="Headfirst Design Pattern",published=True,author=author)
        self.db.save(book)


        authors=self.db.get_all(Author)
        # print(authors)
        assert len(authors)==2

        books=self.db.get_all(Book)
        assert len(books)==2

        book=self.db.get_by_id(Book,1)
        assert book is not None


    def test_get_by_id(self):
        author1=Author(name="Garry C.",age=45)
        self.db.save(author1)
        book1=Book(title="The house of dragon",published=True,author=author1)
        self.db.save(book1)

        authtor_1_fetched=self.db.get_by_id(Author,author1.id)
        book_1_feteched=self.db.get_by_id(Book,book1.id)
        
        assert book_1_feteched.published==book1.published
        assert  book_1_feteched.title==book1.title
        assert book_1_feteched.id==book1.id
        assert book_1_feteched.author._data==author1._data

    def teardown_class(self):
        self.db.connection.close()
        os.remove("./test.db")


class TestSqliteORMUpdate:
    def setup_method(self):
        self.db=Database("./test.db")
        self.db.create(Author)
        self.db.create(Book)

    def teardown_method(self):
        self.db.connection.close()
        os.remove("./test.db")


    def test_db_connection(self):
        assert isinstance(self.db.connection,sqlite3.Connection)
        # assert db.tables==[]

    def test_update_sql(self):
        author1=Author(name="Garry C.",age=45)
        self.db.save(author1)
        book1=Book(title="The house of dragon",published=True,author=author1)
        self.db.save(book1)

        authtor_to_update:Author=self.db.get_by_id(Author,author1.id)
        authtor_to_update.name="Garry C. Mertin"
        authtor_to_update.age=50
        update_sql,column_names,params=authtor_to_update._get_update_sql()

        assert update_sql=="UPDATE author SET name = ?, age = ? WHERE id = ?;"
        assert column_names==["name = ?","age = ?"]
        assert params==["Garry C. Mertin",50,authtor_to_update.id]

        book_to_update:Book=self.db.get_by_id(Book,book1.id)
        update_sql,column_names,params=book_to_update._get_update_sql()
        assert update_sql=="UPDATE book SET title = ?, published = ?, author_id = ? WHERE id = ?;"
        assert column_names==["title = ?","published = ?","author_id = ?"]
        assert params==["The house of dragon",True,authtor_to_update.id,book_to_update.id]

    
    def test_update_author(self):
        author=Author(name="Garry C.",age=45)
        self.db.save(author)
        
        authtor_to_update:Author=self.db.get_by_id(Author,author.id)
        authtor_to_update.name="Garry C. Mertin"
        authtor_to_update.age=50

        self.db.update(authtor_to_update)

        updated_author_fetched:Author=self.db.get_by_id(Author,author.id)

        print(authtor_to_update)
        print(updated_author_fetched)
        assert JSONUtils.to_dict(updated_author_fetched)==JSONUtils.to_dict(authtor_to_update)

    def test_update_book(self):
        author=Author(name="Garry C.",age=45)
        self.db.save(author)

        author2=Author(name="Robert C Martin", age=60)
        self.db.save(author2)

        book=Book(title="The house of dragon",published=True,author=author)
        self.db.save(book)

        book_to_update:Book=self.db.get_by_id(Book,book.id)
        book_to_update.title="Teach yourself C"
        book_to_update.author=author2

        self.db.update(book_to_update)

        updated_book_fetched:Book=self.db.get_by_id(Book,book.id)

        assert updated_book_fetched.title=="Teach yourself C"
        assert updated_book_fetched.author.name=="Robert C Martin"
        assert JSONUtils.to_dict(updated_book_fetched.author)==JSONUtils.to_dict(author2)
        assert JSONUtils.to_dict(updated_book_fetched)==JSONUtils.to_dict(book_to_update)
 

class TestSqliteORMDelete:

    def setup_method(self):
        self.db=Database("./test.db")
        self.db.create(Author)
        self.db.create(Book)

    def teardown_method(self):
        self.db.connection.close()
        os.remove("./test.db")

    def test_delete_sql(self):
        author=Author(name="Garry C.",age=45)
        self.db.save(author)

        # author2=Author(name="Robert C Martin", age=60)
        # self.db.save(author2)

        # book=Book(title="The house of dragon",published=True,author=author)
        # self.db.save(book)
        sql,params=author._get_delete_sql(author.id)
        assert sql=="DELETE FROM author WHERE id = ?;"
        assert params==[author.id]

    def test_delete_author(self):
        author=Author(name="Garry C.",age=45)
        self.db.save(author)
        
        self.db.delete(Author,author.id)

        with pytest.raises(RecordNotFound,
                           match=f"Table {Author.__name__} with id {author.id} not found"
                           ):
            self.db.get_by_id(Author,author.id)

         



    