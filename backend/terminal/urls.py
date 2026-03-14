from django.urls import path
from . import views

urlpatterns = [
    path("run/",     views.run_command),
    path("history/", views.get_history),
    path("cwd/",     views.get_cwd),
]