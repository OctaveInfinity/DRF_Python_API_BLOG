from rest_framework import serializers
from django.contrib.auth.models import User

from .models import BlogPost



class BlogPostSerializer(serializers.HyperlinkedModelSerializer):
    owner       = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model   = BlogPost
        fields  = ['url', 'id', 'title', 'content', "like", 'owner']



class UserSerializer(serializers.HyperlinkedModelSerializer):
    blogposts   = serializers.HyperlinkedRelatedField(
                                            many=True,
                                            view_name='blogpost-detail',
                                            read_only=True
                                            )
    class Meta:
        model   = User
        fields  = ['url', 'id', 'username', 'email', 'blogposts']