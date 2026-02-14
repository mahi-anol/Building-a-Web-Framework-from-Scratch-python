from Framework import wsgi_framework
from Framework.middlewares import ErrorHandlerMiddleware
from pathlib import Path

cwd=Path(__file__).resolve().parent

app=wsgi_framework(template_dir=f'{cwd}/templates')

exception_handler_middleware=ErrorHandlerMiddleware(
    app=app
)