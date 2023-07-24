from django.urls import path

from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
from .views import UserRegisterView, profile

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("profile/", profile, name="profile"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path(
        "logout/", LogoutView.as_view(template_name="users/logout.html"), name="logout"
    ),
]
