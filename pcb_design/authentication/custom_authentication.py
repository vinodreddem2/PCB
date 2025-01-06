from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):        
        user, token = super().authenticate(request)

        # Check if the user is logged out
        if user and user.is_logged_out:
            raise AuthenticationFailed("User is logged out")

        return user, token