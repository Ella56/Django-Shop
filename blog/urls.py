from django.urls import path , include 
from .views import BlogView, BlogDetailView, CreateCommentView,CreateReplyView


app_name = "blog"



urlpatterns = [
    path('', BlogView.as_view(), name='blog'),
    path('category/<str:tag>', BlogView.as_view(), name= "blog-category"),
    path('blog-details/<int:pk>', BlogDetailView.as_view(), name="blog-details"),
    path('blog-details/add_reply/<int:pk>',CreateReplyView.as_view(),name='add-reply',),
    path('blog-details/add_comments/<int:pk>',CreateCommentView.as_view(),name='add-comment',),
    # path('blogs/add-reply/<int:pk>',CreateReplyView.as_view(),name='add-reply',),

    
]