from django.urls import path
from .views import *





app_name = "product"



urlpatterns = [
    path("",ProductView.as_view(),name='products'),
    path("list/",ProductListView.as_view(),name= 'product-list'),
    path("product-detail/<int:pk>", ProductDetailView.as_view(), name="product-detail"),

    
]