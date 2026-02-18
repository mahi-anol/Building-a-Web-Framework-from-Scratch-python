from mahi_wsgi_web_framework.exceptions import ResponseError
from mahi_wsgi_web_framework.constants import HttpStatus

class ResourceNotFoundException(ResponseError):
    def __init__(self,message="Resource not Found"):
        super().__init__(message,HttpStatus.METHOD_NOT_ALLOWED)


class UnathorizedResponseException(ResponseError):
    def __init__(self,message="You are not authorized to access this resource"):
        super().__init__(message,HttpStatus.UNAUTHORIZED)



