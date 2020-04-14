from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import BlogPost


class BlogPostsTests(APITestCase):

    def setUp(self):
        user = User.objects.create(username = 'testuser1')
        user.set_password("secret")
        user.save()
        token = Token.objects.create(user=user)

        blogpost = BlogPost.objects.create(owner   = user,
                                           title   = 'First title', 
                                           content = 'First content',
                                           like   = 1,
                                           )
     

    def test_single_user(self):
        """ Ensure a test-database has 1 user.
        """
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)


    def test_single_blogpost(self):
        """ Ensure a test-database has 1 blogpost.
        """
        blogpost_count = BlogPost.objects.count()
        self.assertEqual(blogpost_count, 1)


    def test_get_list_of_blogposts(self):
        """ Ensure an api can get a list of blogposts.
        """
        url = reverse("blogpost-list")
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
    

    def test_get_first_blogpost(self):
        """ Ensure an api can get a first blogpost.
        """
        blogpost = BlogPost.objects.first()
        url = blogpost.get_api_url()
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)


    def test_post_blogpost_without_user(self):
        """ Ensure an api cann't post a new blogpost without credentials.
        """
        user = self.client.force_authenticate(user=None)
        data = {"title": "Unauthorized creation"}
        url = reverse("blogpost-list")
        r = self.client.post(url, data)
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_blogpost_without_user(self):
        """ Ensure an api cann't update a new blogpost without credentials.
        """
        user = self.client.force_authenticate(user=None)
        blogpost = BlogPost.objects.first()
        url = blogpost.get_api_url()
        data = {"title": "Unauthorized changes"}
        r = self.client.put(url, data)
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_post_blogpost_with_user(self):
        """ Ensure an api can create a new blogpost with user credentials.
        """
        token = Token.objects.get(user__username='testuser1')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        data = {"title": "Created"}
        url = reverse("blogpost-list")
        r = self.client.post(url, data)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.json()['title'],  "Created") 
        self.assertEqual(BlogPost.objects.count(), 2)
        

    def test_update_blogpost_with_user(self):
        """ Ensure an api can update a blogposts with user credentials.
        """
        token = Token.objects.get(user__username='testuser1')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        data = {"title": "Updated"}
        blogpost = BlogPost.objects.first()
        url = blogpost.get_api_url()
        r = self.client.put(url, data)
        self.assertEqual(r.status_code, status.HTTP_200_OK)


    def test_user_ownership(self):
        """ Ensure only owner can update a blogpost.
        """
        user2 = User.objects.create(username='testuser2')
        token = Token.objects.create(user=user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        blogpost = BlogPost.objects.first()
        self.assertNotEqual(user2.username, blogpost.owner)
        url = blogpost.get_api_url()
        data = {"title": "Alien"}
        r = self.client.put(url, data)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        
        
    def test_user_login_and_update_blogpost(self):
        """ Ensure user can login and update its blogpost.
        """
        data = {'username': 'testuser1', 'password': 'secret'}
        url = reverse("rest_framework:login")
        r = self.client.post(url, data)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        token = Token.objects.get(user__username='testuser1')
        if token is not None:
            blogpost = BlogPost.objects.first()
            url = blogpost.get_api_url()
            data = {"title"  : "Changed title",
                    "content": "Changed content",
                    "likes"  : 5,
                    }
            self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
            r = self.client.put(url, data)
            self.assertEqual(r.status_code, status.HTTP_200_OK)