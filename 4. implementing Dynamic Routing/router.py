from common_handlers import Handlers

class RouteManager:
    def __init__(self):
        self.routes={}
    
    def register(self,path,handler):
        if path in self.routes:
            raise RuntimeError(f"Path: {path} already bind to another handler")
        self.routes[path]=handler

    def dispatch(self,environ,start_response):
        path=environ.get("PATH_INFO","/")
        handler=self.routes.get(path,Handlers.url_not_found_handler)
        response=handler(environ,start_response)
        # raise RuntimeError("Just a test exception")
        return response