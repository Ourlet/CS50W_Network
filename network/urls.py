
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.create_post, name="post"),
    path("profile/<str:profile>", views.profile_details, name="profile"),

    # API Routes
    path("profile/<str:profile>/add_follower",
         views.add_follower, name="follow"),
    path("profile/<str:profile>/remove_follower",
         views.remove_follower, name="unfollow")
]
