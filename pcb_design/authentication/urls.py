from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import LoginView, LogoutView, UserAPIView,UserRegistrationView,UserProfileView


# write code for router and add it to the urlpatterns
# router = DefaultRouter()
# router.register('auth/register', UserRegistrationView, basename='user-registration')
# router.register('auth/users', UserAPIView, basename='users')
# router.register('auth/login', LoginView, basename='login')
# router.register('auth/logout', LogoutView, basename='logout')
# urlpatterns = router.urls
urlpatterns = [
    path('auth/register/', UserRegistrationView.as_view(), name='user-registration'),
    # path('auth/users/', UserAPIView.as_view(), name='users'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
     path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
     path('profile/', UserProfileView.as_view(), name='user-profile'),
]