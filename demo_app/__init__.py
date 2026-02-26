from mahi_wsgi_web_framework import wsgi_framework
from mahi_wsgi_web_framework.middlewares import ErrorHandlerMiddleware,ReqResLoggingMiddleware,ExecTimeMiddleware
from pathlib import Path
from mahi_wsgi_web_framework.command_handlers import CommonHandlers
from demo_app.middlewares import TokenMiddleware
from mahi_wsgi_web_framework.orm.sqlite_orm import Database
from demo_app.models.book import Book

cwd=Path(__file__).resolve().parent
app=wsgi_framework(template_dir=f'{cwd}/templates',static_dir=f'{cwd}/static')
app.add_middleware(ReqResLoggingMiddleware)
app.add_middleware(ExecTimeMiddleware)
app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(TokenMiddleware)

#Register Database Here
db=Database("./test.db")

#code first approch
# create tbales nd all on the fly
# Create book table
db.create(Book)

# app.add_exception_handler(handler=CommonHandlers.generic_exception_handler)
# exception_handler_middleware=ErrorHandlerMiddleware(
#     app=app
# )