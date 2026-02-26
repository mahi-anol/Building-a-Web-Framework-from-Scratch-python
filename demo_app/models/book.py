# from typing import NamedTuple
# class Book(NamedTuple):
#     id:int
#     name:str
#     author:str
from mahi_wsgi_web_framework.orm.sqlite_orm import Table,PrimaryKey,Column,ForeignKey,Database

class Book(Table):
    id=PrimaryKey(int,auto_increment=True)
    name=Column(str)
    author=Column(str)

