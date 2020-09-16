from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from rest_framework import generics, permissions

from .models import Product
from .serializers import ProductSerializer


class ProductList(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

