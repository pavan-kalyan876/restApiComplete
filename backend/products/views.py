from django.shortcuts import render
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404


# ListCreateAPIView is a generic view that combines both listing a collection
# of model instances (GET) and creating a new instance (POST) in a single API endpoint
class ProductCreateAPI(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def performCreateMethod(self, serializer):
        # serializer.save(user=self.request.user)
        # print(serializer.validated_data)
        title = serializer.validated_data.get("title")  # validating the data
        content = serializer.validated_data.get("content") or None
        if content is None:
            content = title

        serializer.save(content=content)


# as_view it converts class based view into a function based
product_list_create_view = ProductCreateAPI.as_view()


# it retrieves only single object
class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup field


# args allows a function to accept any number of positional arguments. These arguments are passed as a tuple.
# kwargs allows a function to accept any number of keyword arguments (arguments passed as key-value pairs)
# These arguments are passed as a dictionary

@api_view(["GET", "POST"])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method

    if method == "GET":
        if pk is not None:
            # Detail view
            obj = get_object_or_404(Product, pk=pk)# If object doesn't exist, raise 404
            data = ProductSerializer(obj).data
            return Response(data)
        else:
            # List view
            queryset = Product.objects.all()
            data = ProductSerializer(queryset, many=True).data
            return Response(data)

    if method == "POST":
        # Create an item
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get("title")
            content = serializer.validated_data.get("content", title)  # Default content to title if not provided
            serializer.save(content=content)
            return Response(serializer.data)  # Return created data with 201 status
        return Response({"detail": "Invalid data"})
