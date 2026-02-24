from mahi_wsgi_web_framework.orm.sqlite_orm import Database
from tests.test_orm.conftest import Author,Book
import sqlite3
class TestSqliteORM:
    def test_db_connection(self):
        db=Database("./test.db")
        assert isinstance(db.connection,sqlite3.Connection)
        # assert db.tables==[]

    def test_create_table(self):
        db=Database("./test.db")
        db.create(Author)
        db.create(Book)
        db_tables=db.tables
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