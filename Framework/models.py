from typing import Optional
import inspect
class RouteDefination:
    def __init__(self,handler,allowed_methods:Optional[list]=None,kwargs=None):
        self.handler=handler
        self.allowed_methods=allowed_methods or ['GET',"POST","PUT","PATCH","DELETE"]
        self.kwargs=kwargs or {}
    def is_valid_methods(self,method:str)->bool:
        return method in self.allowed_methods
    
    def add_kwargs(self,kwargs:dict):
        self.kwargs.update(kwargs)

    def is_class_based_handler(self):
        return inspect.isclass(self.handler)