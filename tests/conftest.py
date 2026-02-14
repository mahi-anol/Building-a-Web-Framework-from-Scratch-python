from Framework import wsgi_framework
import pytest
from requests import Session as RequestSession
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter
from tests.constants import BASE_URL
from Framework.middlewares import ErrorHandlerMiddleware
from pathlib import Path

class TFramework(wsgi_framework):
    def test_session(self,base_url=BASE_URL):
        session=RequestSession()
        session.mount(prefix=base_url,adapter=RequestsWSGIAdapter(app=ErrorHandlerMiddleware(self)))
        return session
    
@pytest.fixture
def app()->TFramework:
    cwd=Path(__file__).resolve().parent
    return TFramework(template_dir=f"{cwd}/templates")

@pytest.fixture
def client(app:TFramework):
    return app.test_session()
## mod 1
# @pytest.fixture
# def app()->wsgi_framework:
#     return wsgi_framework()

