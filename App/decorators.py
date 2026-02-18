from webob import Request
from App.constants import STATIC_TOKEN
from App.exceptions import UnathorizedResponseException

def login_required(handler):
    def wrapped_handler(request:Request,*args,**kwargs):
        if not request.token or request.token!=STATIC_TOKEN:
            raise UnathorizedResponseException("Invalid Token")
        
        return handler(request,*args,**kwargs)
    return wrapped_handler