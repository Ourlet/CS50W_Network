
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.create_post, name="post"),
    path("profile/<str:profile>", views.profile, name="profile"),

    # API Routes
    path("update/<str:profile>",
         views.update_profile, name="update_profile"),
    path("update/<int:post>", views.update_post, name="update_post")
]
