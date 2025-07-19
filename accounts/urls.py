from django.urls import path , include 
from .views import LoginView,RegisterView,ViewProfile,UpdateProfileView



app_name = "accounts"



urlpatterns = [
    path("login/", LoginView.as_view(),name='login'),
    path("signup/",RegisterView.as_view(),name='signup'),
    path("view-profile/", ViewProfile.as_view(),name="view-profile"),
    path("edit-profile/<int:pk>/",UpdateProfileView.as_view(),name='edit-profile'),

]