from webob import Request

class ErrorHandlerMiddleware:
    def __init__(self,app,ExceptionHandler:callable ):
        self.wrapped_app=app
        self.ExceptionHandler=ExceptionHandler
        print("Middle were is running...")
    def __call__(self,envrion,start_response,*args,**kwds):
        try:
            return self.wrapped_app(envrion,start_response,*args,**kwds)
        except Exception as e:
            request=Request(envrion)
            response=self.ExceptionHandler(request,e)
            return response(envrion,start_response)