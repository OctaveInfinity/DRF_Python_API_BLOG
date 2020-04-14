from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import BlogPost


class BlogPostsTests(APITestCase):

    def setUp(self):
        user = User.objects.create(username = 'testuser1')
        user.set_password("secret")
        user.save()
        blogpost = BlogPost.objects.create(owner   = user,
                                           title   = 'First title', 
                                           content = 'First content',
                                           like   = 1,
                                           )
     

    def test_single_user(self):
        """ Ensure a test database has 1 user.
        """
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)


    def test_single_blogpost(self):
        """ Ensure a test database has 1 blogpost.
        """
        blogpost_count = BlogPost.objects.count()
        self.assertEqual(blogpost_count, 1)


    def test_get_list(self):
        """ Ensure an api can get a list of blogposts.
        """
        url = reverse("blogpost-list")
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
    

    def test_get_item(self):
        """ Ensure an api can get a first blogpost.
        """
        blogpost = BlogPost.objects.first()
        url = blogpost.get_api_url()
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
