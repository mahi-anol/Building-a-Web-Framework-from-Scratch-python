from mahi_wsgi_web_framework.orm.sqlite_orm import Database
from tests.test_orm.conftest import Author,Book
import sqlite3
class TestSqliteORM:
    def test_db_connection(self):
        db=Database("./test.db")
        assert isinstance(db.connection,sqlite3.Connection)
        assert db.tables==[]

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

        assert Book.Author.table==Author
        assert Author.age.sql_type=="INTEGER"

    def test_table_creation_sql(self):
        assert Author._get_create_sql() == "CREATE TABLE IF NOT EXISTS author (id INTEGER PRIMARY KEY AUTOINCREMENT, age INTEGER, name TEXT);"
        assert Book._get_create_sql() == "CREATE TABLE IF NOT EXISTS book (id INTEGER PRIMARY KEY AUTOINCREMENT, author_id INTEGER, published INTEGER, title TEXT);"