from common_handlers import Handlers
from webob import Request,Response
from helpers import normalize_request_url
from parse import parse
import inspect
class RouteManager:
    def __init__(self):
        self.routes={}
    
    def register(self,path,handler):
        if path in self.routes:
            raise RuntimeError(f"Path: {path} already bind to another handler")
        self.routes[path]=handler

    def _find_handler(self,request_path)->tuple:
        request_path=normalize_request_url(request_path)

        if request_path in self.routes:
            handler=self.routes[request_path]
            return handler,{}
        
        # # URl that contains path variable
        for path,handler in self.routes.items():
            parsed=parse(path,request_path)
            if parsed:
                return handler,parsed.named

        return Handlers.url_not_found_handler,{}
    
    def _get_class_based_handler(self,request:Request,handler_class)->callable:
        handler_instance=handler_class()
        method=request.method.lower()
        handler_fn=getattr(handler_instance,method,Handlers.method_not_allowed)
        return handler_fn

    def dispatch(self,http_request:Request):
        handler,kwargs=self._find_handler(http_request.path)
        if inspect.isclass(handler):
            handler=self._get_class_based_handler(http_request,handler)

        return handler(http_request,**kwargs)