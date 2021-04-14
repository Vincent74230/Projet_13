"""url paths of useraccount app"""

from django.urls import path
from . import views

app_name = "useraccount"
urlpatterns = [
    path("", views.index, name="index"),
]
