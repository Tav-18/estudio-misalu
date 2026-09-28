from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("proyecto/", views.project_info, name="project_info"),
    path("area-interna/", views.internal_area, name="internal_area"),
    path("area-interna/login/", views.internal_login, name="internal_login"),
    path("area-interna/salir/", views.internal_logout, name="internal_logout"),
    path("area-interna/trabajadores/nuevo/", views.worker_form, name="worker_create"),
    path("area-interna/trabajadores/<int:pk>/editar/", views.worker_form, name="worker_edit"),
    path("area-interna/trabajadores/<int:pk>/eliminar/", views.worker_delete, name="worker_delete"),
    path("api/chat/", views.chat_api, name="chat_api"),
]
