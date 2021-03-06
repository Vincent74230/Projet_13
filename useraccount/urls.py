"""url paths of useraccount app"""
from django.urls import path
from .views import Index, ActivateAccount
from . import views

app_name = "useraccount"
urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("login", views.login_page, name="login"),
    path("logout", views.log_out, name="logout"),
    path("activate/<uidb64>/<token>", ActivateAccount.as_view(), name='activate'),
    path("myaccount", views.my_account, name='myaccount'),
    path("score", views.score, name='score'),
]
