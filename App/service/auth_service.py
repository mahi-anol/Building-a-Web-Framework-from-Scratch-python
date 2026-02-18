from App.models.token import Token
from App.constants import STATIC_TOKEN
class AuthService:
    def get_auth_token(self,**kwargs)->Token:
        return Token(STATIC_TOKEN)