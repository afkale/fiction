"""
URL configuration for fiction project.

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
from django.urls import include, path

from rest_framework import routers
from drf_spectacular import views as drfs_views
from rest_framework_simplejwt import views as jwt_views

from tutorial.quickstart import views as example_views


router = routers.DefaultRouter()
router.register(r"users", example_views.UserViewSet)
router.register(r"groups", example_views.GroupViewSet)

schema_urls = [
    path("schema/", drfs_views.SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/",
        drfs_views.SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "redoc/",
        drfs_views.SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

token_urls = [
    path("", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", jwt_views.TokenVerifyView.as_view(), name="token_verify"),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/", include(schema_urls)),
    path("api/token/", include(token_urls)),
]
