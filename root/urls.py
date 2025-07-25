from django.urls import path , include 
from .views import HomeView,ContactView,AboutView



app_name = 'root'


urlpatterns =[
    path('', HomeView.as_view(),name='home'),
    path('contact/', ContactView.as_view(),name='contact'),
    path('about-us/', AboutView.as_view(),name='about'),
]



