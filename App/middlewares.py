from mahi_wsgi_web_framework.middlewares import Middleware
import re
from webob import Request
class TokenMiddleware(Middleware):
    _regex=re.compile(r"^Token: (\w+)$")
    def process_request(self,req:Request):
        header=req.headers.get("Authorization","")
        match=self._regex.match(header)
        token=match and match.group(1) or None
        req.token=token