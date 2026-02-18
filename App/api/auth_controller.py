from App import app
from webob import Request
from mahi_wsgi_web_framework.models import JSONResponse
from App.service.auth_service import AuthService
from App.models.token import Token
service=AuthService()
@app.route('/token',allowed_methods=["POST"])
def get_token(request:Request)->JSONResponse:
    token:Token=service.get_auth_token(**request.json)
    return JSONResponse(
        token._asdict()
    )