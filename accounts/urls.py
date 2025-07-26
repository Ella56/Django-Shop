from django.urls import path , include 
from .views import LoginView, SignupView, ViewProfile, UpdateProfileView, SetAddressView, get_city



app_name = "accounts"



urlpatterns = [
    path("login/", LoginView.as_view(),name='login'),
    path("signup/",SignupView.as_view(),name='signup'),
    path("view-profile/", ViewProfile.as_view(),name="view-profile"),
    path("edit-profile/<int:pk>/",UpdateProfileView.as_view(),name='edit-profile'),
    path("view-profile/<int:pk>/", ViewProfile.as_view(), name='view-profile'),
    path("profile/addresses/", SetAddressView.as_view(), name='addresses'),

]