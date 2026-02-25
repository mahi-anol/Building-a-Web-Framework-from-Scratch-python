from mahi_wsgi_web_framework.orm.sqlite_orm import Database
from tests.test_orm.conftest import Author,Book
import sqlite3
import os
class TestSqliteORM:
    def __init__(self):
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

    
    def test_row_insertion_query(self):
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


    def teardown_class(self):
        self.db.connection.close()
        os.remove("./test.db")
