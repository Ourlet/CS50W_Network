import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.core.paginator import Paginator
from django.db.models import Count


from .models import Follower, Post, User, Like
from .forms import createPostForm


def index(request):
    posts = Post.objects.annotate(num_likes=Count(
        'liked')).order_by('-creation_date').all()
    paginator = Paginator(posts, 3)  # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "post": createPostForm(),
        'page_obj': page_obj,
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


@ csrf_exempt
@ login_required
def profile(request, profile):

    poster = get_object_or_404(User, username=profile)
    profile_posts = Post.objects.annotate(num_likes=Count(
        'liked')).order_by(
        '-creation_date').filter(poster=poster)
    paginator = Paginator(profile_posts, 3)  # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "poster": poster,
        'page_obj': page_obj
    })


@ csrf_exempt
@ login_required
def update_profile(request, profile):

    # Identify who is consulting the profile
    viewer = request.user

    if request.method == "GET":

        try:
            # Get data from User and Follower DB
            profile = User.objects.get(username=profile)
            follower = Follower.objects.filter(followed=profile).all().count()
            followed = Follower.objects.filter(follower=profile).all().count()
            profilePosts = Post.objects.order_by(
                '-creation_date').filter(poster=profile)
            serialized_profilePosts = serialize("json", profilePosts)
            serialized_profilePosts = json.loads(serialized_profilePosts)
            print(serialized_profilePosts)
            following = Follower.objects.filter(
                follower=viewer, followed=profile).exists()
            ownProfile = viewer == profile

        except User.DoesNotExist:
            return JsonResponse({"message": "Profile doesn't exist."}, status=404)

        return JsonResponse({
            "username": profile.username,
            "firstname": profile.first_name,
            "lastname": profile.last_name,
            "accountCreated": profile.date_joined,
            "follower": follower,
            "followed": followed,
            "posts": serialized_profilePosts,
            "isFollowing": following,
            "isOwnProfile": ownProfile
        }, safe=False, status=201)

    if request.method == "POST":

        # Get the data of the profile visited
        profileViewed = get_object_or_404(User, username=profile)

        # Avoid users to follow themselves
        if profileViewed == viewer:
            return JsonResponse({"message": "User can't follow itself."}, status=400)

        # Prevent user to follow multiple times the same profile
        if Follower.objects.filter(follower=viewer, followed=profileViewed):
            return JsonResponse({"message": "Profile already followed."}, status=400)

        # Save the Follower and Followed in the DB
        follower = Follower(follower=viewer, followed=profileViewed)
        follower.save()

        return JsonResponse({"Following": "Follower added successfully."}, status=201)

    if request.method == "DELETE":
        # Get the data of the profile visited
        profileViewed = get_object_or_404(User, username=profile)

        # Avoid users to unfollow themselves
        if profileViewed == viewer:
            return JsonResponse({"message": "User can't unfollow itself."}, status=400)

        # Prevent user to unfollow multiple times the same profile
        if not Follower.objects.filter(follower=viewer, followed=profileViewed):
            return JsonResponse({"message": "Profile not followed."}, status=400)

        # Delete Follower and Followed in the DB
        Follower.objects.filter(
            follower=viewer, followed=profileViewed).delete()

        return JsonResponse({"Following": "Follower removed successfully."}, status=201)

# Create a get post API to get all data relative to a post


@ csrf_exempt
def get_post(request, profile=None):
    viewer = request.user

    if profile is None:
        posts = Post.objects.all()

    else:
        poster = get_object_or_404(User, username=profile)
        posts = list(Post.objects.filter(poster=poster))
        print(posts)

    serialized_profilePosts = serialize("json", posts)
    serialized_profilePosts = json.loads(serialized_profilePosts)
    print(serialized_profilePosts)

    return JsonResponse({
        "posts": serialized_profilePosts,
    }, safe=False, status=201)


@ csrf_exempt
@ login_required
def update_post(request, post_id):
    viewer = request.user
    post = get_object_or_404(Post, pk=post_id)

    # Get the data of the post viewer

    if request.method == "POST":

        # Avoid users to follow themselves
        if post.poster == viewer:
            return JsonResponse({"message": "User can't like its own post."}, status=400)

        # Prevent user to follow multiple times the same profile
        if Like.objects.filter(liker=viewer, liked=post):
            return JsonResponse({"message": "Post already liked."}, status=400)

        # Save the Follower and Followed in the DB
        like = Like(liker=viewer, liked=post)
        like.save()

        return JsonResponse({"Like": "User liked the post."}, status=201)

    if request.method == "DELETE":

        # Avoid users to unfollow themselves
        if post.poster == viewer:
            return JsonResponse({"message": "User can't unfollow itself."}, status=400)

        # Prevent user to unlike multiple times the same post
        if not Like.objects.filter(liker=viewer, liked=post):
            return JsonResponse({"message": "Post already unliked."}, status=400)

        # Delete Follower and Followed in the DB
        Like.objects.filter(
            liker=viewer, liked=post).delete()

        return JsonResponse({"Like": "User unliked the post."}, status=201)
