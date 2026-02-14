from Framework.command_handlers import CommonHandlers
from Framework.routing_manager import RouteManager
from webob import Request,Response

class wsgi_framework:
    def __init__(self):
        self.routing_manager=RouteManager()
    
    def __call__(self,environ,start_response):
        http_request=Request(environ)
        response:Response=self.routing_manager.dispatch(http_request)
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