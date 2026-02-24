import sqlite3
import inspect

class Column:
    def __init__(self,column_type):
        self.type=column_type

    @property
    def sql_type(self):
        type_map={
            int: "INTEGER",
            float: "REAL",
            str: "TEXT",
            bytes: "BLOB",
            bool: "INTEGER", #  0 or 1
        }
        return type_map[self.type]
    
class PrimaryKey(Column):
    def __init__(self,column_type=int,auto_increment=True):
        self.auto_increment=auto_increment
        super().__init__(column_type)

class TableMeta(type):
    def __new__(cls, name, bases, attrs):
        columns={}
        for key,value in attrs.items():
            if isinstance(value,Column):
                columns[key]=value

        # cls._columns=columns
        attrs["_columns"]=columns
        return super().__new__(cls,name,bases,attrs)
class Table(metaclass=TableMeta):
    @classmethod
    def _get_create_sql(cls):
        CREATE_TABLE_SQL="CREATE TABLE IF NOT EXISTS {name} ({fields});"
        fields=[]
        # for name,field in inspect.getmembers(cls):
        for name, field in cls._columns.items():
            if isinstance(field,PrimaryKey):
                sql=f"{name} {field.sql_type} PRIMARY KEY"
                if field.auto_increment:
                    sql+=" AUTOINCREMENT"
                fields.append(sql)
            elif isinstance(field,ForeignKey):
                fields.append(f"{name}_id INTEGER")
            elif isinstance(field,Column):
                fields.append(f"{name} {field.sql_type}")
        table_name=cls.__name__.lower()
        fields=", ".join(fields)
        return CREATE_TABLE_SQL.format(name=table_name,fields=fields)

class ForeignKey(Column):
    def __init__(self,table:type[Table],column_type=int):
        self.table=table
        super().__init__(column_type)

    
class Database:
    def __init__(self, path: str):
        self.path = path
        self.connection=sqlite3.Connection(path)
    @property
    def tables(self):
        result_set=self.connection.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        # return result_set
        return [rs[0] for rs in result_set]
        # return []
    
    def create(self,table:type[Table]):
        raw_sql=table._get_create_sql()
        self.connection.execute(raw_sql)