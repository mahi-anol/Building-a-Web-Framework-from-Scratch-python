from parse import parse
from webob.request import Request
from Framework.command_handlers import CommonHandlers
import inspect


def normalize_request_url(url:str)->str:
    if url!="/" and url.endswith("/"):
        return url[:-1]
    return url

class RoutingHelper:
    @classmethod
    def _find_handler(cls,routes:dict,request:Request)->tuple:
        requested_path=normalize_request_url(request.path)

        if requested_path in routes:
            return routes[requested_path],{}
        
        for path,handler in routes.items():
            parsed=parse(path,requested_path)

            if parsed:
                return handler,parsed.named
            
        return CommonHandlers.url_not_found_handler,{}
    
    @classmethod
    def _find_class_based_handler(cls,handler,request:Request,kwargs:dict)->tuple:
        handler_instance=handler()
        function_name=request.method.lower()
        handler_fn=getattr(handler_instance,function_name,None)

        if not handler_fn:
            return CommonHandlers.method_not_allowed_handler,{}
        return handler_fn,kwargs
    
    @classmethod
    def get_handler(cls,routes:dict,request:Request)->tuple:
        handler,kwargs=cls._find_handler(routes,request)
        if inspect.isclass(handler):
            handler,kwargs=cls._find_class_based_handler(handler,request,kwargs)
        return handler,kwargs
