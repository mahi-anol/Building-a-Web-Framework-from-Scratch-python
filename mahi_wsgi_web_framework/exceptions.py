from mahi_wsgi_web_framework.constants import HttpStatus
from webob import Request
class ResponseError(Exception):
    def __init__(self, message:str, http_status:str):
        self.message=message
        self.htto_status=http_status
        super().__init__(self.message)


class MethodNotAllowed(ResponseError):
    def __init__(self, request:Request):
        message=f"{request.method} request is not allowed for {request.path}"
        super().__init__(message,HttpStatus.METHOD_NOT_ALLOWED)