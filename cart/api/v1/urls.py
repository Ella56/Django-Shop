from django.urls import path
from .views import *



urlpatterns = [
    # path("cart", BlogApiView.as_view({"get" : "list", "post" : "create"}),name = "cart"),
    # path("blog-post/<int:pk>",BlogApiView.as_view({"get" : "retrieve", "put" : "update", "patch" : "update", "delete" : "destroy"}), name="blog_post"),
    # path("blog/<int:blog_pk>/comments/", CommentView.as_view({'get': 'list','post': 'create'}), name ="comments"),
    # path("comment/<int:pk>", CommentView.as_view({"get" : "retrieve", "put" : "update", "patch" : "update", "delete" : "destroy"}), name="single-comment"),

]