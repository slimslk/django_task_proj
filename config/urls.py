"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    info=openapi.Info(
        title='Tasks Management System Open API',
        default_version='1',
        description='''API for tasks management system. 
        Here you can find all endpoints responsible for system management.
        Through this API you can manage tasks, subtasks and categories. 
        Also here is endpoints for getting and refreshing JWT token.
        V1 - it's old API version implemented via Django REST api_view decorator and usual APIView class.
        V2 - it's new API version implemented via Django REST generic APIView and ModelViewSet classes.
        ''',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(
            name='Dimm',
            email='dimm@dimmid.net',
        ),
        license=openapi.License(
            name="MIT License"
        )
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('task_app.urls')),
    path('api/v2/', include('task_app.url_api_v2')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=1000)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=1000)),
]
