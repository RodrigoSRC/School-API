from django.urls import path
from . import views


urlpatterns = [
    path("accounts/", views.AccountView.as_view()),
    path("login/", views.LoginJWTView.as_view())
]