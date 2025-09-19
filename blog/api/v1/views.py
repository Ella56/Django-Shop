from rest_framework.viewsets import ViewSet, ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from .permissions import IsAdminOrReadOnly
from .serializer import BlogSerializer, CommentSerializer
from blog.models import Blog, Blog_Comment
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from accounts.models import Profile
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser



class BlogApiView(ModelViewSet):
    permission_classes =[IsAdminOrReadOnly]
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    search_fields = ["title", "category__category"]


class CommentView(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Blog_Comment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    
    def perform_create(self, serializer):
        # Automatically associate the comment with the logged-in user
        blog = get_object_or_404(Blog, pk=self.kwargs.get("blog_pk"))
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(blog=blog, name=profile)