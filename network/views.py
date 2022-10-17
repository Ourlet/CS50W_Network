import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse

from .models import Follower, Post, User
from .forms import createPostForm


def index(request):
    return render(request, "network/index.html", {
        "posts": Post.objects.order_by('-creation_date').all(),
        "post": createPostForm()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def create_post(request):
    if request.method == "POST":
        poster = User.objects.get(username=request.user)

        form = createPostForm(request.POST)
        if form.is_valid():
            post = form.cleaned_data["content"]
            new_post = Post(poster=poster, content=post)
            new_post.save()
    return HttpResponseRedirect(reverse("index"))


def profile_details(request, profile):

    # Identify who is consulting the profile
    viewer = request.user

    try:
        # Get data from User and Follower DB
        p = User.objects.get(username=profile)
        follower = Follower.objects.filter(followed=p).all().count()
        followed = Follower.objects.filter(follower=p).all().count()

    except User.DoesNotExist:
        return render(request, "network/error_handling.html",
                      {
                          "code": 404,
                          "message": "Profile doesn't exist"
                      })

    else:
        return render(request, "network/profile.html", {
            "profile": p,
            "follower": follower,
            "followed": followed,
            "posts": Post.objects.order_by('-creation_date').filter(poster=p),
            "isFollowing": Follower.objects.filter(
                follower=viewer, followed=p).exists(),
            "isOwnProfile": viewer == p
        })


def add_follower(request, profile):

    # Identify who is consulting the profile
    viewer = request.user

    if request.method == "POST":

        # Get the data of the profile visited
        profileViewed = get_object_or_404(User, username=profile)

        # Avoid users to follow themselves
        if profileViewed == viewer:
            return render(request, "network/error_handling.html", {
                "code": 400,
                "message": "User can't follow itself."
            })

        # Prevent user to follow multiple times the same profile
        if Follower.objects.filter(follower=viewer, followed=profileViewed):
            return render(request, "network/error_handling.html", {
                "code": 400,
                "message": "Profile already followed"
            })

        # Save the Follower and Followed in the DB
        follower = Follower(follower=viewer, followed=profileViewed)
        follower.save()

    return HttpResponseRedirect(reverse("profile", args=(profile,)))


def remove_follower(request, profile):

    # Identify who is consulting the profile
    viewer = request.user

    if request.method == "POST":
        # Get the data of the profile visited
        profileViewed = get_object_or_404(User, username=profile)

        # Avoid users to unfollow themselves
        if profileViewed == viewer:
            return render(request, "network/error_handling.html", {
                "code": 400,
                "message": "User can't unfollow itself."
            })

        # Prevent user to unfollow multiple times the same profile
        if not Follower.objects.filter(follower=viewer, followed=profileViewed):
            return render(request, "network/error_handling.html", {
                "code": 400,
                "message": "Profile not followed"
            })

        # Delete Follower and Followed in the DB
        Follower.objects.filter(
            follower=viewer, followed=profileViewed).delete()

    return HttpResponseRedirect(reverse("profile", args=(profile,)))
