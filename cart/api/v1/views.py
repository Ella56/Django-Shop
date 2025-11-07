from rest_framework.viewsets import ViewSet, ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from .permissions import IsAdminOrReadOnly
from .serializer import *
from blog.models import Blog, Blog_Comment
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from accounts.models import Profile
from django.shortcuts import get_object_or_404



class CartApiView(ModelViewSet):
    pass