from parse import parse
from webob.request import Request
from Framework.command_handlers import CommonHandlers
import inspect
from Framework.models import RouteDefination

def normalize_request_url(url:str)->str:
    if url!="/" and url.endswith("/"):
        return url[:-1]
    return url

class RoutingHelper:
    @classmethod
    def _find_handler(cls,routes:dict,request:Request)->RouteDefination:
        requested_path=normalize_request_url(request.path)

        if requested_path in routes:
            return routes[requested_path]
            # return routes[requested_path],{}
        
        for path,route_def in routes.items():
            parsed=parse(path,requested_path)

            if parsed:
                # return handler,parsed.named
                route_def.add_kwargs(parsed.named)
                return route_def
            
        return RouteDefination(CommonHandlers.url_not_found_handler)
    
    @classmethod
    def _find_class_based_handler(cls,request:Request,route_def:RouteDefination)->tuple:
        handler_instance=route_def.handler()
        function_name=request.method.lower()
        handler_fn=getattr(handler_instance,function_name,None)

        if not handler_fn:
            return RouteDefination(CommonHandlers.method_not_allowed_handler)
        # return handler_fn,kwargs
        return RouteDefination(handler_fn,kwargs=route_def.kwargs)
    
    @classmethod
    def get_route_defination(cls,routes:dict,request:Request)->RouteDefination:
        route_def:RouteDefination=cls._find_handler(routes,request)
        if route_def.is_class_based_handler():
            return cls._find_class_based_handler(request,route_def)
        
        if not route_def.is_valid_methods(request.method):
            return RouteDefination(CommonHandlers.method_not_allowed_handler)
        
        return route_def
