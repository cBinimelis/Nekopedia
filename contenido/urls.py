from django.urls import path
from . import views

app_name = "contenido"

urlpatterns = [
    path("", views.home, name="home"),
]
