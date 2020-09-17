from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from rest_framework import generics, permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product
from .serializers import ProductSerializer


class ListProductsPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class ProductList(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('name',)
    search_fields =('name',)
    pagination_class = ListProductsPagination


class ProductCreate(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        description = request.data.get('description')
        price = request.data.get('price')
        if name is None:
            raise ValidationError({'name': 'You must provide a product name'})
        if description is None:
            raise ValidationError({'description': 'You must provide a product description'})
        if price is None:
            raise ValidationError({'price': 'You must provide a price'})
        return super().create(request, *args, **kwargs)


class ProductRetriveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Product.objects.all()
    lookup_field = 'product_id'
    serializer_class = ProductSerializer

    def delete(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete('products_data_{}'.format(product_id))
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            from django.core.cache import cache
            product = response.data
            cache.set('products_data_{}'.format(product['product_id']), {
                'name': product['name'],
                'description': product['description'],
                'price': product['price']
            })
            return response

