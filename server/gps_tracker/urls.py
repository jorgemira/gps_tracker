from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from .gps_tracker import urls, viewsets

router = routers.DefaultRouter()
router.register(r"locations", viewsets.LocationCreateAPIView)

urlpatterns = [
    path("api/", include(router.urls)),
    path("auth/", obtain_auth_token, name="auth"),
    path("api/panic/", viewsets.panic, name="panic"),
    path("", include(urls)),
]
