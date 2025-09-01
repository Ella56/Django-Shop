from rest_framework.viewsets import ViewSet, ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from .permissions import IsAdminOrReadOnly
from .serializer import BlogSerializer
from blog.models import Blog



class BlogApiView(ModelViewSet):
    permission_classes =[IsAdminOrReadOnly]
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    search_fields = ["title", "category__category"]