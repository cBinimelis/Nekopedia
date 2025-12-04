from django.urls import path
from . import views

app_name = "contenido"

urlpatterns = [
    path("", views.listado_contenido, name="listado"),
    path("<int:pk>/", views.detalle_contenido, name="detalle"),
]
