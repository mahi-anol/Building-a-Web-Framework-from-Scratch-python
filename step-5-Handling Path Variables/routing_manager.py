from common_handlers import Handlers
from webob import Request,Response
from helpers import normalize_request_url
from parse import parse
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
    def dispatch(self,http_request:Request):
        handler,kwargs=self._find_handler(http_request.path)
        return handler(http_request,**kwargs)