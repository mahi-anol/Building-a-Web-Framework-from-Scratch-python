from Framework.command_handlers import CommonHandlers
from webob import Request,Response
from typing import TYPE_CHECKING
from Framework.logger import create_logger
import time
from Framework.exceptions import ResponseError
if TYPE_CHECKING:
    from Framework.framework import wsgi_framework

logger=create_logger(__name__)

class Middleware:
    def __init__(self,app:"wsgi_framework"):
        self.app=app

    def __call__(self, environ, start_response):
        request=Request(environ)
        response=self.handle_request(request)
        return response(environ,start_response)
    
    def add(self,middleware_cls)->None:
        logger.info(f"{middleware_cls.__name__}(app={self.app.__class__.__name__})")
        self.app=middleware_cls(app=self.app)

    def process_request(self,req:Request)->None:
        logger.info(f"{self.__class__.__name__}::process_request")
    
    def process_response(self,req:Request,resp:Response)->None:
        logger.info(f"{self.__class__.__name__}::process_response")

    def handle_request(self,request:Request)->Response:
        self.process_request(request)
        response=self.app.handle_request(request)
        self.process_response(request,response)
        return response



class ErrorHandlerMiddleware(Middleware):
    def handle_request(self,request:Request)->Response:
        try:
            return super().handle_request(request)
        except ResponseError as e:
            return CommonHandlers.handle_response_error(request,e)
        except Exception as e:
            return CommonHandlers.generic_exception_handler(request,e)


class ReqResLoggingMiddleware(Middleware):
    def process_request(self,req:Request)->None:
        super().process_request(req)
        logger.info(f"Processing Request: {req.path}")

    def process_response(self,req:Request,resp:Response)->None:
        super().process_response(req,resp)
        logger.info(f"Processing Response: {req.path}")

class ExecTimeMiddleware(Middleware):

    def process_request(self, req):
        req.start_time=time.time()
    
    def process_response(self, req, resp):
        duration=time.time()-req.start_time
        resp.headers['X-Response-Time']=f"{duration:.4f}s"
        logger.info(f"Total Processing Time: {duration:.4f}")
##mod1

# class ErrorHandlerMiddleware:
#     def __init__(self,
#                  app:'wsgi_framework',
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