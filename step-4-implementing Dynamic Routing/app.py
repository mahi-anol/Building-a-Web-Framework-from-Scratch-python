from middlewares import ErrorHandlerMiddleware
from common_handlers import Handlers
from router import RouteManager



class Application:
    def __init__(self):
        self.routing_manager=RouteManager()
        
    def __call__(self,environ,start_response,*args,**kwargs):
        return self.routing_manager.dispatch(environ,start_response)
    
    def route(self,path):
        def decorator(handler):
            self.routing_manager.register(path,handler)
            return handler
        return decorator


app=Application()
middleware=ErrorHandlerMiddleware(
    app=app,ExceptionHandler=Handlers.generic_exception_handler
)