from django.urls import path , include 
from .views import HomeView,ContactView



app_name = 'home'


urlpatterns =[
    path('', HomeView.as_view(),name='home'),
    path('contact/', ContactView.as_view(),name='contact'),


]



