
from django.urls import path

from . import views

urlpatterns = [
    path("index/<str:page>", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<str:username>", views.profile, name="profile"),
    path("people/<str:username>/<str:page>", views.following, name="following"),
    path("emails", views.compose, name="compose"),
    path("emails/<int:email_id>", views.email, name="email"),
]
