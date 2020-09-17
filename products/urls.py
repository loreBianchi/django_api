from django.urls import path
from .views import ProductList, ProductCreate, ProductRetriveUpdateDestroy

urlpatterns = [
    path('all/', ProductList.as_view(), name='product-list'),
    path('new/', ProductCreate.as_view(), name='product-create'),
    path('<int:product_id>/', ProductRetriveUpdateDestroy.as_view(), name='product-detail')
]