import sqlite3
import inspect
from typing import TypeVar
from mahi_wsgi_web_framework.orm.exeptions import RecordNotFound
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

        table_cls=super().__new__(cls,name,bases,attrs)
        table_cls._columns=columns
        return table_cls
    
class Table(metaclass=TableMeta):
    def __init__(self,**kwargs):
        self._data={
            "id":None,# For Data.
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
        # slightly buggy though as there is param mirroring in __dict__ and _data
        super().__setattr__(key,value)
        if key in self._data:
            self._data[key]=value
           
    @property
    def __dict__(self):
        return self._data
    
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
    
    def _get_update_sql(self)->str:
        #"UPDATE author SET name = ?, age = ? WHERE id = ?;"
        UPDATE_SQL_TEMPLATE="UPDATE {name} SET {fields} WHERE id = ?;"
        table_name=self.__class__.__name__.lower()
        fields=[]
        values=[]
        for name, field in self._columns.items():
            if isinstance(field,PrimaryKey):
                continue
            if isinstance(field,ForeignKey):
                fields.append(name+'_id = ?')
                field_value:T=getattr(self, name)
                values.append(field_value.id)
            elif isinstance(field,Column):
                fields.append(name+" = ?")
                field_value=getattr(self,name)
                values.append(field_value)

        values.append(getattr(self,'id'))
        sql=UPDATE_SQL_TEMPLATE.format(
            name=table_name,
            fields=", ".join(fields),
        )
        return sql, fields,values
    @classmethod
    def _get_delete_sql(cls,id:int):
        # DELETE FROM author WHERE id =1;
        DELETE_SQL_TEMPLATE="DELETE FROM {name} WHERE id = ?;"
        table_name=cls.__name__.lower()
        params=[id]
        sql=DELETE_SQL_TEMPLATE.format(name=table_name)
        return sql,params

class ForeignKey(Column):
    def __init__(self,table:type[Table],column_type=int):
        self.table=table
        super().__init__(column_type)

T=TypeVar("T", bound=Table)
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
    
    def create(self,table:type[T]):
        raw_sql=table._get_create_sql()
        self.connection.execute(raw_sql)

    def save(self,table_instance:Table):
        sql,values=table_instance._get_insert_sql()
        cursor=self.connection.execute(sql,values)
        table_instance._data["id"]=cursor.lastrowid # thats how id gets the value.
        # table_instance.id=cursor.lastrowid
        self.connection.commit()

    ### Design choice 2
    def get_all(self,table_type:type[T])->list[T]:
        sql,column_names=table_type._get_select_all_sql()
        rows=self.connection.execute(sql).fetchall()
        result=[]
        for row in rows:
            # Map to python type class
            kwargs={}
            instance=self._to_class_type(table_type=table_type,column_names=column_names,row=row)
            result.append(instance)
        return result
    
    def get_by_id(self,table_type:type[T],id:int)->T:
        sql,column_names,params=table_type._get_select_by_id_sql(id)
        row=self.connection.execute(sql,params).fetchone()
        if not row:
            raise RecordNotFound(f"Table {table_type.__name__} with id {id} not found")
        instance=self._to_class_type(table_type=table_type,column_names=column_names,row=row)
        return instance
    
    def _get_fk_by_id(self,parent_table_type:type[T],fk_field_name:str,fk_id:int)->T:
        fk:ForeignKey=parent_table_type._columns[fk_field_name]
        fk_instance=self.get_by_id(fk.table,id=fk_id)
        return fk_instance

    def _to_field_name(self,column_name:str)->str:
        if column_name.endswith("_id"):
            return column_name[:-3]
        return column_name
    
    def _to_class_type(self,table_type:type[T],column_names:list[str],row:tuple)->T:
        # for 1 row
        kwargs={}
        for column_name,col_value in zip(column_names,row):
            field_name=self._to_field_name(column_name)
            column:Column=table_type._columns[field_name]
            if isinstance(column,ForeignKey):
                fk_instance=self._get_fk_by_id(parent_table_type=table_type,
                                                fk_field_name=field_name,
                                                fk_id=col_value)
                kwargs[field_name]=fk_instance
            else:
                kwargs[field_name]=column.type(col_value)

        instance=table_type(**kwargs)
        return instance
    
    def update(self,table:T)->None:
        update_sql,column_names,params=table._get_update_sql()
        self.connection.execute(update_sql,params)# params contains id.
        self.connection.commit()

    def delete(self,table_type:type[T],id)->None:
        delete_sql,params=table_type._get_delete_sql(id)
        self.connection.execute(delete_sql,params)
        self.connection.commit()

