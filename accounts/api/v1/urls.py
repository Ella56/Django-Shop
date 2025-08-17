from django.urls import path , include 
from .views import *



urlpatterns = [
    path("signup/", SignUpApiView.as_view(), name="signup"),


]