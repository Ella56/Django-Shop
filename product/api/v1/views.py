from rest_framework.viewsets import ViewSet, ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from .permissions import IsAdminOrReadOnly
from .serializer import ProductSerializer
from product.models import Product



class ProductApiView(ModelViewSet):
    permission_classes =[IsAdminOrReadOnly]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    search_fields = ["name", "category__name"]