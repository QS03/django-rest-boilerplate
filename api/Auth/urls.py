from django.urls import path
from api.Auth.views import LogoutView, LoginView, RefreshView, RegisterViewSet, ProfileViewSet, UserViewSet

urlpatterns = [
    # re_path("", include('djoser.urls'), name="djoser"),
    path("auth/register/", RegisterViewSet.as_view({'post': 'create'}), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/refresh/", RefreshView.as_view(), name="refresh"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
]

urlpatterns += [
    path("users/", UserViewSet.as_view(
        {
            'get': 'list',
        }
    ), name="users"),
    path("users/<int:id>", UserViewSet.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }
    ), name="user-details"),
]

urlpatterns += [
    path("profile/", ProfileViewSet.as_view(
        {
            'get': 'me',
            'put': 'me',
            'patch': 'me',
            'delete': 'me'
        }
    ), name="profile"),
]
