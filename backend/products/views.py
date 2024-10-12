from django.shortcuts import render
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer

# Create your views here.


class ProductCreateAPI(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def performCreateMethod(self, serializer):
        # serializer.save(user=self.request.user)
       # print(serializer.validated_data)
        title = serializer.validated_data.get("title") # validating the data 
        content = serializer.validated_data.get("content") or None
        if content is None:
            content = title

        serializer.save(content=content)


# as_view it converts class based view into a function based
product_create_view = ProductCreateAPI.as_view()


# it retrieves only single object
class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup field


