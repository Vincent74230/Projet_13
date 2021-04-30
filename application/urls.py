"""url paths of application app"""

from django.urls import path
from . import views

app_name = "application"
urlpatterns = [
    path("", views.index, name="index"),
    path("search_results", views.search_results, name="search_results"),
]
