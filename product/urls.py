from django.urls import path
from .views import *





app_name = "product"



urlpatterns = [
    path("",ProductView.as_view(),name='products'),
    path("list/",ProductListView.as_view(),name= 'product-list'),
    path("product-detail/<int:pk>", ProductDetailView.as_view(), name="product-detail"),
    path('list/',ProductListView.as_view(), name='products-list'),
    path('list/category/', ProductListView.as_view(), name='products-list-by-category'),
    path('list/category-detail/', ProductListView.as_view(), name='products-list-by-detail-category'),
    path('list/price-range/', ProductListView.as_view(), name='products-list-by-price-range'),
    path('list/with-guarantee/',ProductListView.as_view(),name='products-list-by-guarantee'),
    path('add-comment/<int:pk>/',ProductCommentView.as_view(),name='product-comment',),
    path('add-replay/<int:pk>/', ProductReplyView.as_view(), name='add-replay'),
    path('list/search/', ProductListView.as_view(), name='product-by-search'),

    
]