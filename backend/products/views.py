from django.shortcuts import render
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer

# Create your views here.


class ProductCreateAPI(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# as_view it converts class based view into a function based
product_create_view = ProductCreateAPI.as_view()


# it retrieves only single object
class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
