from django.urls import path
from rest_framework import renderers
from rest_framework.urlpatterns import format_suffix_patterns

from .views import BlogPostViewSet, UserViewSet, api_root


blogpost_list   = BlogPostViewSet.as_view({ 'get': 'list',
                                            'post': 'create' })  

blogpost_detail = BlogPostViewSet.as_view({ 'get': 'retrieve',
                                            'put': 'update',
                                            'patch': 'partial_update',
                                            'delete': 'destroy' })
                                          

user_list       = UserViewSet.as_view({ 'get': 'list',
                                        'post': 'create' })

user_detail     = UserViewSet.as_view({ 'get': 'retrieve',
                                        'put': 'update',
                                        'patch': 'partial_update',
                                        'delete': 'destroy' })


# API endpoints
urlpatterns = format_suffix_patterns([
    path('', api_root),
    
    path('blogposts/',          blogpost_list,      name='blogpost-list'),
    path('blogposts/<int:pk>/', blogpost_detail,    name='blogpost-detail'),
    
    path('users/',              user_list,          name='user-list'),
    path('users/<int:pk>/',     user_detail,        name='user-detail'),
])