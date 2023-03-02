from django.urls import re_path, include


api_urlpatterns = [
    re_path('', include('api.Auth.urls', ), name='auth'),
]
