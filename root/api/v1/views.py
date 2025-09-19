from rest_framework.viewsets import ViewSet, ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from .permissions import IsAdminOrReadOnly
from .serializer import *
from accounts.models import User,Profile
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser




class TeamView(ModelViewSet):
    permission_classes =[IsAdminOrReadOnly]
    serializer_class = TeamSerializer
    queryset = Team.objects.all()


class ContactView(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ContactSerializer
    queryset = ContactUs.objects.all()



class FaqView(ModelViewSet):
    permission_classes =[IsAdminOrReadOnly]
    serializer_class = FaqSerializers
    queryset = Faq.objects.all()