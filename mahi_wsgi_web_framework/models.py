from typing import Optional
import inspect
from mahi_wsgi_web_framework.constants import HttpStatus,ContentType
from webob import Response
from typing import Any,Sequence
from enum import Enum
import json
class RouteDefination:
    def __init__(self,handler,allowed_methods:Optional[list]=None,kwargs=None):
        self.handler=handler
        self.allowed_methods=allowed_methods or ["GET","POST","PUT","PATCH","DELETE"]
        self.kwargs=kwargs or {}
    def is_valid_methods(self,method:str)->bool:
        return method in self.allowed_methods
    
    def add_kwargs(self,kwargs:dict):
        self.kwargs.update(kwargs)

    def is_class_based_handler(self):
        return inspect.isclass(self.handler)
    
class TextResponse(Response):
    def __init__(self,content:str,status:str=HttpStatus.OK,**kwargs):
        super().__init__(text=content,status=status,content_type=ContentType.TEXT,**kwargs)

class JSONResponse(Response):
    def __init__(self,content:dict|Any,status:str=HttpStatus.OK,**kwargs):
        # if not isinstance(content,dict):
        #     if hasattr(content,"__dict__"):
        #         content=content.__dict__
        content=self._to_dict(content)
        super().__init__(json=content,status=status,content_type=ContentType.JSON,**kwargs)

    def _to_dict(self,content:dict|list|Any):
        if content is None:
            return None
        if isinstance(content,(str,int,float,bool)):
            return content
        if isinstance(content,Enum):
            return content.value
        if isinstance(content,dict):
            return {
                key:self._to_dict(value)
                for key,value in content.items()
            }
        if hasattr(content,"__dict__"):
            return self._to_dict(content.__dict__)
        if isinstance(content,(list,tuple,set,Sequence)):
            return [self._to_dict(item) for item in content]
        return content
class HTMLResponse(Response):
    def __init__(self,content:str,status:str=HttpStatus.OK,**kwargs):
        super().__init__(body=content,status=status,content_type=ContentType.HTML,**kwargs)
