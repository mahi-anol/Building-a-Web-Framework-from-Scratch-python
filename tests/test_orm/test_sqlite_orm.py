from mahi_wsgi_web_framework.orm.sqlite_orm import Database
import sqlite3
class TestSqliteORM:
    def test_db_connection(self):
        db=Database("./test.db")
        assert isinstance(db.connection,sqlite3.Connection)
        assert db.tables==[]
