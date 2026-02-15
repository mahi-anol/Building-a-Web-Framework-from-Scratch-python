from Framework import wsgi_framework
import pytest
from requests import Session as RequestSession
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter
from tests.constants import BASE_URL
from Framework.middlewares import ErrorHandlerMiddleware
from pathlib import Path
from Framework.command_handlers import CommonHandlers
class TFramework(wsgi_framework):
    def test_session(self,base_url=BASE_URL):
        session=RequestSession()
        session.mount(prefix=base_url,adapter=RequestsWSGIAdapter(app=self))
        return session
    
@pytest.fixture
def app()->TFramework:
    cwd=Path(__file__).resolve().parent
    app=TFramework(template_dir=f"{cwd}/templates",static_dir=f"{cwd}/static")
    # app.add_exception_handler(handler=CommonHandlers.generic_exception_handler)
    return app

@pytest.fixture
def client(app:TFramework):
    return app.test_session()
## mod 1
# @pytest.fixture
# def app()->wsgi_framework:
#     return wsgi_framework()


@pytest.fixture
def static_dir(tmpdir_factory):
    return tmpdir_factory.mktemp('static')
