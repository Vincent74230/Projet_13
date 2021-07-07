"""url paths of application app"""

from django.urls import path
from . import views

app_name = "application"
urlpatterns = [
    path("", views.index, name="index"),
    path("search_results", views.search_results, name="search_results"),
    path("mentions_legales", views.mentions_legales, name='mentions_legales'),
    path("A_propos", views.about, name='about'),
]
