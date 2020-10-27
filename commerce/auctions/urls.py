from django.urls import path
from django.contrib import admin


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/", views.create, name="create"),
    path("<str:name>/", views.page, name = "page"),
    path("wishlist", views.wishlist, name="wishlist"),
    path("categories", views.categories, name="categories"),
    path('admin/', admin.site.urls),
]