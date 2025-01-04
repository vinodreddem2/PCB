from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.conf import settings

class CustomAuthentication(TokenAuthentication, SessionAuthentication):
    """
    Custom authentication
    """
    token_auth = TokenAuthentication()
    session_auth = SessionAuthentication()

    def authenticate(self, request):
        
        DEBUG = settings.__dict__['_wrapped'].__dict__['DEBUG']

        if DEBUG:
            return self.token_auth.authenticate(request)
        else:
            return self.session_auth.authenticate(request)