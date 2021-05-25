"""url paths of useraccount app"""
from django.urls import path
from .views import Index, ActivateAccount
from . import views

app_name = "useraccount"
urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("login", views.login_page, name="login"),
    path("activate/<uidb64>/<token>", ActivateAccount.as_view(), name='activate'),
]
