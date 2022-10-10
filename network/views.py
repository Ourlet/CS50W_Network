from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

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


def poster_details(request, user):

    poster = get_object_or_404(User, username=user)
    follower = Follower.objects.filter(followed=poster).all().count()
    followed = Follower.objects.filter(follower=poster).all().count()

    return render(request, "network/user.html", {
        "user": poster,
        "follower": follower,
        "followed": followed
    })
