from django.urls import path, include
from .views import (
    RegisterAPI,
    UpdateUserAPI,
    UsersListAPI,
    UserDetailsAPI,
    PermissionsListAPI,
    PermissionDetailAPI,
    ChangeEmailView,
    ResetPasswordForm,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Authentication Urls
    path('auth/signup', RegisterAPI.as_view(), name="signup"),
    path('auth/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Profile Urls
    path('account/update', UpdateUserAPI.as_view(), name="update_account"),
    path('account/password-reset', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('account/password-reset-form', ResetPasswordForm.as_view(), name='password_reset_form'),
    path('account/change-email', ChangeEmailView.as_view(), name='change_email'),

    # Users urls
    path('users', UsersListAPI.as_view(), name="list_users"),
    path('users/<int:pk>', UserDetailsAPI.as_view(), name="user_detail"),

    # Permission urls
    path('permissions', PermissionsListAPI.as_view(), name="list_permissions"),
    path('permissions/<int:pk>', PermissionDetailAPI.as_view(), name="permission_detail"),
]
