from django.urls import path
from .views import *


urlpatterns= [
    path('contact/', ContactView.as_view({"get": "list", "post": "create"}), name="contact"),
    path('contact/<int:pk>/', ContactView.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}), name="contact-detail"),
    path('team/', TeamView.as_view({"get": "list", "post": "create"}), name="team"),
    path('team/<int:pk>/', TeamView.as_view({"get": "list", "post": "create"}), name="team-detail"),
    path('faq/', FaqView.as_view({"get": "list", "post": "create"}), name="faq"),
    path('faq/<int:pk>/', FaqView.as_view({"get": "list", "post": "create"}), name="faq-detail"),
]