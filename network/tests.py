from urllib import response
from django.test import TestCase, Client

from .models import Post, User

# Create your tests here.


class PostTestCase(TestCase):

    def setUp(self):

        # Create Users

        u1 = User.objects.create(first_name="u1", username="u1")
        u2 = User.objects.create(first_name="u2", username="u2")

        # Create posts
        p1 = Post.objects.create(
            poster=u1, content="This is the post of poster1")
        p2 = Post.objects.create(
            poster=u2, content="This is the post of poster2")
        p3 = Post.objects.create(
            poster=u1, content="This is the second post of poster1")

    def test_index(self):
        c = Client()
        response = c.get("")
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["posts"].count(), 3)
