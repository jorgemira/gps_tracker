from django.urls import include, path
from rest_framework import routers
from .gps_tracker import views

router = routers.DefaultRouter()
router.register(r'locations', views.LocationCreateAPIView)

urlpatterns = [
    path('', include(router.urls)),
]
