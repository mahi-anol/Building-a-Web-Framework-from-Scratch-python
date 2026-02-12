from Framework import wsgi_framework
from Framework.middlewares import ErrorHandlerMiddleware

app=wsgi_framework()

exception_handler_middleware=ErrorHandlerMiddleware(
    app=app
)