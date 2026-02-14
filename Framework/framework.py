from Framework.command_handlers import CommonHandlers
from Framework.routing_manager import RouteManager
from webob import Request,Response
from jinja2 import Environment,FileSystemLoader
import os
from typing import Optional
class wsgi_framework:
    def __init__(self,template_dir:str|None="templates"):
        self.routing_manager=RouteManager()
        self.template_env=Environment(loader=FileSystemLoader(os.path.abspath(template_dir)))
        self.exception_handler:Optional[callable]=None

    def __call__(self,environ,start_response):
        http_request=Request(environ)
        try:
            response:Response=self.routing_manager.dispatch(http_request)
        except Exception as e:
            if not self.exception_handler:
                raise e
            response:Response=self.exception_handler(http_request,e)

        return response(environ,start_response)
    
    def add_route(self,path:str,handler:callable)->None:
        """
        Django Style explicit route registration
        :type path: str
        :type handler: callable
        """
        self.routing_manager.register(path,handler)

    def route(self,path:str):
        def decorator(handler):
            self.add_route(path,handler)
            return handler
        return decorator
    
    def template(self,template_name:str,context:dict)->str:
        context=context or {}
        return self.template_env.get_template(template_name).render(**context)
    
    def add_exception_handler(self,handler:callable)->None:
        self.exception_handler=handler