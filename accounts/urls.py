from django.urls import path , include 
from .views import *



app_name = "accounts"



urlpatterns = [
    path("login/", LoginView.as_view(),name='login'),
    path("signup/",SignupView.as_view(),name='signup'),
    path("view-profile/", ViewProfile.as_view(),name="view-profile"),
    path("edit-profile/<int:pk>/",UpdateProfileView.as_view(),name='edit-profile'),
    path("view-profile/<int:pk>/", ViewProfile.as_view(), name='view-profile'),
    path("profile/addresses/", SetAddressView.as_view(), name='addresses'),
    path("compare/",CompareView.as_view(), name='user-compare'),
    path("create-compare/", compare_create,name="user-create-compare"),
    path("remove-compare/",compare_remove, name="user-remove-compare"),
    path("favorites/", FavoriteView.as_view(), name="user-favorites"),
    path("create-favorites/", favorites_create, name='user-create-favories'),
    path("remove-favories/<int:pk>/", favorites_remove, name="user-remove-favorites"),

]