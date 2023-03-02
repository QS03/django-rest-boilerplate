from django.contrib import admin
from django.urls import re_path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from api.urls import api_urlpatterns

urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path('drf/', include('rest_framework.urls')),

    # Api
    re_path('api/', include((api_urlpatterns, 'api'), namespace="api")),

    # Schema
    re_path('api/schema', SpectacularAPIView.as_view(api_version='api'), name='api-schema'),

    # Docs
    re_path('api/swagger', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-swagger'),
    re_path('api/redoc', SpectacularRedocView.as_view(url_name='api-schema'), name='api-redoc'),
]
