from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from .views import products, get_products, CategoryList, ProductList

urlpatterns = [
    path('', products),
    path('get-categories', CategoryList.as_view()),
    path('get-products', ProductList.as_view()),
]