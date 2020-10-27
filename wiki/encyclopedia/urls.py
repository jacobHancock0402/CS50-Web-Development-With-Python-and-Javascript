from django.urls import path

from . import views

urlpatterns = [
    path("?q=<str:query>/", views.search, name = "search"),
    path("", views.index, name="index"),
    path("wiki/<str:nam>/", views.get, name = "get"),
    path("random", views.rand, name = "random"),
    path("create/", views.create, name="create"),
    path("edit/<str:page>/", views.edit, name="edit")
]
