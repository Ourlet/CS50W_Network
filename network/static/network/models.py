from enum import auto
from msilib import CAB
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    poster = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="poster")
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return f"{self.id} : {self.content} writen by {self.poster} on {self.creation_date}"


class Like(models.Model):
    liker = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="liker")
    liked = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="liked")
    like_date = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return f"{self.id} : {self.liked} liked by {self.liker}"


class Follower(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower")
    followed = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followed")

    def __str__(self):
        return f"{self.id} : {self.follower} is following {self.followed}"
