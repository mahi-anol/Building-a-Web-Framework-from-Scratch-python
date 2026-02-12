from command_handlers import CommonHandlers
from Framework.routing_manager import RouteManager
from webob import Request,Response

class wsgi_framework:
    def __init__(self):
        self.routing_manager=RouteManager()
    
    def __call__(self,environ,start_response):
        http_request=Request(environ)
        response:Response=self.routing_manager.dispatch(http_request)
        return response
    
    def route(self,path:str):
        def decorator(handler):
            self.routing_manager.register(path,handler)
            return handler
        return decorator