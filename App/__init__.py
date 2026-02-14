from Framework import wsgi_framework
from Framework.middlewares import ErrorHandlerMiddleware
from pathlib import Path
from Framework.command_handlers import CommonHandlers
cwd=Path(__file__).resolve().parent

app=wsgi_framework(template_dir=f'{cwd}/templates')
app.add_exception_handler(handler=CommonHandlers.generic_exception_handler)
exception_handler_middleware=ErrorHandlerMiddleware(
    app=app
)