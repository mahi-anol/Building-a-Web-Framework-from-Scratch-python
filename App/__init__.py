from Framework import wsgi_framework
from Framework.middlewares import ErrorHandlerMiddleware,ReqResLoggingMiddleware,ExecTimeMiddleware
from pathlib import Path
from Framework.command_handlers import CommonHandlers

cwd=Path(__file__).resolve().parent
app=wsgi_framework(template_dir=f'{cwd}/templates',static_dir=f'{cwd}/static')
app.add_middleware(ReqResLoggingMiddleware)
app.add_middleware(ExecTimeMiddleware)
app.add_middleware(ErrorHandlerMiddleware)
# app.add_exception_handler(handler=CommonHandlers.generic_exception_handler)
# exception_handler_middleware=ErrorHandlerMiddleware(
#     app=app
# )