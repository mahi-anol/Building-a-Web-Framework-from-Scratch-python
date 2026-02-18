from mahi_wsgi_web_framework import wsgi_framework
from mahi_wsgi_web_framework.middlewares import ErrorHandlerMiddleware,ReqResLoggingMiddleware,ExecTimeMiddleware
from pathlib import Path
from mahi_wsgi_web_framework.command_handlers import CommonHandlers
from App.middlewares import TokenMiddleware
cwd=Path(__file__).resolve().parent
app=wsgi_framework(template_dir=f'{cwd}/templates',static_dir=f'{cwd}/static')
app.add_middleware(ReqResLoggingMiddleware)
app.add_middleware(ExecTimeMiddleware)
app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(TokenMiddleware)


# app.add_exception_handler(handler=CommonHandlers.generic_exception_handler)
# exception_handler_middleware=ErrorHandlerMiddleware(
#     app=app
# )