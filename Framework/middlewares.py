from Framework.framework import wsgi_framework
from Framework.command_handlers import CommonHandlers
from webob import Request,Response


class Middleware:
    def __init__(self,app:wsgi_framework):
        self.app=app

    def __call__(self, environ, start_response):
        request=Request(environ)
        response=self.handle_request(request)
        return response(environ,start_response)
    def add(self,middleware_cls)->None:
        self.app=middleware_cls(app=self.app)

    def process_request(self,req:Request)->None:
        pass

    def process_response(self,req:Request,resp:Response)->None:
        pass

    def handle_request(self,request:Request)->Response:
        self.process_request(request)
        response=self.app.handle_request(request)
        self.process_response(request,response)
        return response



class ErrorHandlerMiddleware(Middleware):
    def handle_request(self,request:Request)->Response:
        try:
            return super().handler_request(request)
        except Exception as e:
            return CommonHandlers.generic_exception_handler(request,e)

##mod1

# class ErrorHandlerMiddleware:
#     def __init__(self,
#                  app:wsgi_framework,
#                  exception_handler:callable=CommonHandlers.generic_exception_handler
#                 ):
#         self.wrapped_app=app
#         self.exception_handler=exception_handler

#     def __call__(self, environ,start_response):
#         try:
#             return self.wrapped_app(environ,start_response)
#         except Exception as e:
#             request=Request(environ)
#             response=self.exception_handler(request,e)
#             return response(environ,start_response)