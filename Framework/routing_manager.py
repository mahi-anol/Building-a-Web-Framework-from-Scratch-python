from webob import Request

from Framework.helpers import RoutingHelper
from typing import Optional
from Framework.models import RouteDefination
class RouteManager:
    def __init__(self):
        self.routes={}

    def register(self,path,handler,allowed_methods:Optional[list]=None):
        if allowed_methods:
            allowed_methods=[method.upper() for method in allowed_methods]
        if path in self.routes:
            raise RuntimeError(f"Path: {path} already bind to another handler.")
        self.routes[path]=RouteDefination(handler,allowed_methods)

    def dispatch(self,http_request:Request):
        # handler,kwargs=RoutingHelper.get_handler(self.routes,http_request)
        # return handler(http_request,**kwargs)
        route_def:RouteDefination=RoutingHelper.get_route_defination(self.routes,http_request)
        return route_def.handler(http_request,**route_def.kwargs)
    
    
