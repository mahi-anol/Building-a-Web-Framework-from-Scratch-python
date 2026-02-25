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
    def __init__(self,**kwargs):
        self._data={
            "id":None,
        }
        for key,value in kwargs.items():
            self._data[key]=value
        self.id=self._data["id"]
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
    

    def __getattribute__(self, key):
        _data=super().__getattribute__("_data")
        if key in _data:
            return _data[key]

        return super().__getattribute__(key)
        
    def __setattr__(self, key, value):
        super().__setattr__(key,value)
        if key in self._data:
            self._data[key]=value

    
    def _get_insert_sql(self)->tuple[str,list]:
        INSERT_SQL="INSERT INTO {name} ({fields}) VALUES ({placeholders});"
        fields=[]
        placeholders=[]
        values=[]

        for name, field in self._columns.items():
            if isinstance(field,ForeignKey):
                fields.append(name+"_id")
                field_value:Table=getattr(self,name)
                values.append(field_value.id)
                placeholders.append("?")

            elif isinstance(field,Column):
                fields.append(name)
                values.append(getattr(self,name))
                placeholders.append("?")

        fields=", ".join(fields)
        placeholders=", ".join(placeholders)
        table_name=self.__class__.__name__.lower()
        query=INSERT_SQL.format(
            name=table_name,fields=fields,placeholders=placeholders
        )
        return query,values
    @classmethod
    def _get_select_all_sql(cls):
        SELECT_ALL_SQL='SELECT {fields} FROM {table_name};'
        fields=[]
        for name, field in cls._columns.items():
            if isinstance(field,ForeignKey):
                fields.append(name+'_id')
            elif isinstance(field,Column):
                fields.append(name)

        table_name=cls.__name__.lower()
        field_names=fields
        fields=", ".join(fields)
        sql=SELECT_ALL_SQL.format(table_name=table_name,fields=fields)
        return sql,field_names
    
    @classmethod
    def _get_select_by_id_sql(cls,id:int):
        SELECT_ALL_SQL='SELECT {fields} FROM {name} WHERE id=?;'
        table_name=cls.__name__.lower()
        fields=[]

        for name, field in cls._columns.items():
            if isinstance(field,ForeignKey):
                fields.append(name+'_id')
            elif isinstance(field,Column):
                fields.append(name)
        params=[id]
        sql=SELECT_ALL_SQL.format(name=table_name,fields=", ".join(fields))
        return sql,fields,params
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

    def save(self,table_instance:Table):
        sql,values=table_instance._get_insert_sql()
        cursor=self.connection.execute(sql,values)
        table_instance._data["id"]=cursor.lastrowid
        # table_instance.id=cursor.lastrowid
        self.connection.commit()

    # def get_all(self,table_type:type[Table])->list[Table]:
    #     sql,field_names=table_type._get_select_all_sql()
    #     rows=self.connection.execute(sql).fetchall()
    #     result=[]
    #     for row in rows:
    #         instance=table_type()
    #         for field_name,col_value in zip(field_names,row):
    #             setattr(instance,field_name,col_value)
    #         result.append(instance)
    #     return result

    ### Design choice 2
    def get_all(self,table_type:type[Table])->list[Table]:
        sql,field_names=table_type._get_select_all_sql()
        rows=self.connection.execute(sql).fetchall()
        result=[]
        for row in rows:
            kwargs={}
            for field_name,col_value in zip(field_names,row):
                if field_name.endswith("_id"):
                    field_name=field_name[:-3]
                    f_key:ForeignKey=getattr(table_type,field_name)
                    f_table_type=f_key.table
                    f_instance=self.get_by_id(f_table_type,id=col_value)
                    col_value=f_instance
                kwargs[field_name]=col_value
            instance=table_type(**kwargs)
            result.append(instance)
        return result
    
    def get_by_id(self,table_type:type[Table],id:int)->Table:
        sql,field_names,params=table_type._get_select_by_id_sql(id)
        row=self.connection.execute(sql,params).fetchone()
        if not row:
            raise Exception(f"Table {table_type.__name__} with id {id} not found")
        kwargs={}
        for field_name,col_value in zip(field_names,row):
            if field_name.endswith("_id"):
                field_name=field_name[:-3]
                f_key:ForeignKey=getattr(table_type,field_name)
                f_table_type=f_key.table
                f_instance=self.get_by_id(f_table_type,id=col_value)
                col_value=f_instance
            kwargs[field_name]=col_value
        
        instance=table_type(**kwargs)

        return instance