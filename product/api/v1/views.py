from rest_framework.viewsets import ViewSet, ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from .permissions import IsAdminOrReadOnly
from .serializer import ProductSerializer, ProductCommentSerializer
from product.models import Product, Comment
from accounts.models import User,Profile
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser


class ProductApiView(ModelViewSet):
    permission_classes =[IsAdminOrReadOnly]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    search_fields = ["name", "category__name"]



class CommentView(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProductCommentSerializer
    queryset = Comment.objects.all()

    
    def perform_create(self, serializer):
        # Automatically associate the comment with the logged-in user
        product = get_object_or_404(Product, pk=self.kwargs.get("product_pk"))
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(product=product, name=profile)