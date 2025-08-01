from django.urls import path , include 
from .views import BlogView, BlogDetailView


app_name = "blog"



urlpatterns = [
    path('', BlogView.as_view(), name='blog'),
    path('category/<str:tag>', BlogView.as_view(), name= "blog-category"),
    path('blog-details/<int:pk>', BlogDetailView.as_view(), name="blog-details"),

    
]