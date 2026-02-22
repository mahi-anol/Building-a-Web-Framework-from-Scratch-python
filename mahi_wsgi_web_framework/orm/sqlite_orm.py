import sqlite3

class Database:
    def __init__(self, path: str):
        self.path = path
        self.connection=sqlite3.Connection(path)
    @property
    def tables(self):
        return []

class Table:
    pass

class Column:
    def __init__(self,column_type):
        self.column_type=column_type
    @property
    def sql_type(self):
        type_map={
            int: "INTEGER",
            float: "REAL",
            str: "TEXT",
            bytes: "BLOB",
            bool: "INTEGER",
        }
        return type_map[self.sql_type]
    
class PrimaryKey(Column):
    def __init__(self,column_type=int,auto_increment=True):
        self.auto_increment=auto_increment
        super().__init__(column_type)

class ForeignKey(Column):
    def __init__(self,table:type[Table],column_type=int):
        self.table=table
        super().__init__(column_type)