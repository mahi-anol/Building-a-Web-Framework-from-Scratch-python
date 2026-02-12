from webob import Request

from Framework.helpers import RoutingHelper

class RouteManager:
    def __init__(self):
        self.routes={}

    def register(self,path,handler):
        if path in self.routes:
            raise RuntimeError(f"Path: {path} already bind to another handler")
        self.routes[path]=handler

    def dispatch(self,http_request:Request):
        handler,kwargs=RoutingHelper.get_handler(self.routes,http_request)
        return handler(http_request,**kwargs)
    
