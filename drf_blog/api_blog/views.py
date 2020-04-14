from django.contrib.auth.models import User

from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import BlogPost
from .permissions import IsOwnerOrReadOnly
from .serializers import BlogPostSerializer, UserSerializer



@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'blogposts': reverse('blogpost-list', request=request, format=format)
    })



class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    queryset            = User.objects.all()
    serializer_class    = UserSerializer
    permission_classes  = [permissions.IsAuthenticated]



class BlogPostViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    queryset            = BlogPost.objects.all()
    serializer_class    = BlogPostSerializer
    permission_classes  = [permissions.IsAuthenticatedOrReadOnly,
                            IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
