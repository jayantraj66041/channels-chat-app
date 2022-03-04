from django.urls import path
from app.views import Home, Login, Signup, Dashboard

urlpatterns = [
    path("", Home.as_view(), name="homepage"),
    path("login/", Login.as_view(), name="login"),
    path("signup/", Signup.as_view(), name="signup"),
    path("dashboard/", Dashboard.as_view(), name="dashboard"),
]
