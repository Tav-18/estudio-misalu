from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("proyecto/", views.project_info, name="project_info"),
    path("api/chat/", views.chat_api, name="chat_api"),
]
