class ErrorHandlerMiddleware:
    def __init__(self,app,ExceptionHandler:callable ):
        self.wrapped_app=app
        self.ExceptionHandler=ExceptionHandler
    def __call__(self,envrion,start_response,*args,**kwds):
        try:
            return self.wrapped_app(envrion,start_response,*args,**kwds)
        except Exception as e:
            return self.ExceptionHandler(envrion,start_response,e)