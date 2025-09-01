from django.urls import path
from .views import *



urlpatterns = [
    path("blog", BlogApiView.as_view({"get" : "list", "post" : "create"}),name = "blog"),
    path("blog-post/<int:pk>",BlogApiView.as_view({"get" : "retrieve", "put" : "update", "patch" : "update", "delete" : "destroy"}), name="blog_post"),


]