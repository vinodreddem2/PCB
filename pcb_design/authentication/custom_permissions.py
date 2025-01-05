from rest_framework import permissions
from django.contrib.auth.models import Permission
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class IsAuthorized(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        Checking if user has permissions to access this viewset
        Permission should be assigned to the user or to the assigned groups
        Example:
            get_customerdetails_view
            post_customerregistration_view
            put_customerupdate_view
            delete_customerfile_view
        """
        # Temporary - Returning True
        return True

        view_name = view.__class__.__name__.lower()
        request_method = request.method.lower()
        permission_codename = request_method + "_" + view_name + "_view"

        user = request.user
        user_groups = user.groups.all()


        # Checking if user groups has permissions assigned or not
        for each in user_groups:
            if each.permissions.filter(codename = permission_codename).exists():
                return True
        
        # Checking if user has direct permissions assigned
        if Permission.objects.filter(user__username=user.username, codename = permission_codename).exists():
            return True
        
        return False
    

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):        
        user, token = super().authenticate(request)

        # Check if the user is logged out
        if user and user.is_logged_out:
            raise AuthenticationFailed("User is logged out")

        return user, token
