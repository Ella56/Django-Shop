from django.urls import path
from .views import *



urlpatterns = [
    path("products", ProductApiView.as_view({"get" : "list", "post" : "create"}),name = "all_products"),
    path("product/<int:pk>",ProductApiView.as_view({"get" : "retrieve", "put" : "update", "patch" : "update", "delete" : "destroy"}), name="single_product"),


]