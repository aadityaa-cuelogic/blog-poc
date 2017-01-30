from django.test import TestCase
from .models import Post, Comment, Category, Likes, Imagepost
from django.test.utils import setup_test_environment
from django.test import Client
from django.urls import reverse
# Create your tests here.

def create_post(title, category, desc, img=None):
    return Post.objects.create()

class PostMethodTests(TestCase):
    def test_createPost_method_invalide_input(self):
        """
            createPost() method should return false if invalid inpute is
            passed
        """
