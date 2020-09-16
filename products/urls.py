from django.urls import path
from .views import ProductList

urlpatterns = [
    path('all/', ProductList.as_view(), name='product-list')
]