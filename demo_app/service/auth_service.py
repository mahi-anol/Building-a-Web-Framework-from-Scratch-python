from demo_app.models.token import Token
from demo_app.constants import STATIC_TOKEN
class AuthService:
    def get_auth_token(self,**kwargs)->Token:
        return Token(STATIC_TOKEN)