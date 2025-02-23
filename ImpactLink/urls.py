"""
URL configuration for ImpactLink project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include , re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Define the schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Your Project API",
        default_version='v1',
        description="API documentation for your Django project",
        terms_of_service="https://www.yourwebsite.com/terms/",
        contact=openapi.Contact(email="your-email@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,  # False means only authenticated users can see the docs
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('linker/', include('linker.urls')),
    path('redirect/', include('redirect.urls')),
    # Swagger UI (Browsable Interface)
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),

    # ReDoc (Alternative API documentation)
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),

    # Raw API schema in JSON/YAML format
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
