
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
    path("update_profile/<str:profile>",
         views.update_profile, name="update_profile"),
    path("get_post/", views.get_post, name="post"),
    path("get_post/<str:profile>", views.get_post, name="post_profile"),
    path("update_post/<int:post_id>", views.update_post, name="update_post"),
    # path("get_like/<int:post_id>", views.get_like, name="like")
]
