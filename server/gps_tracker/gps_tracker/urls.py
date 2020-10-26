from django.urls import path
from . import views

urlpatterns = [
    path("login", views.login, name="login"),
    path("show_map", views.show_map, name="show_map"),
    path("switch_panic", views.switch_panic, name="switch_panic"),
]
