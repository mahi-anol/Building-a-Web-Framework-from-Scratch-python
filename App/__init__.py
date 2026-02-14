from Framework import wsgi_framework
from Framework.middlewares import ErrorHandlerMiddleware

app=wsgi_framework(template_dir='./App/templates')

exception_handler_middleware=ErrorHandlerMiddleware(
    app=app
)