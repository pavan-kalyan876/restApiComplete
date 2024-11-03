from django.shortcuts import render
from rest_framework import authentication, generics, mixins, permissions
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
    authentication_classes = [authentication.SessionAuthentication]

    permission_classes = [
        permissions.DjangoModelPermissions
    ]  

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


product_detail_view = ProductDetailAPIView.as_view()


class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"  # lookup_field = "pk" ensures that the view will retrieve objects based on their primary key

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title


product_update_view = ProductUpdateAPIView.as_view()


class ProductDeleteAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"

    def perform_destroy(self, instance):
        # Perform any custom operations before deletion if needed
        instance.delete()  # Call instance.delete() to delete the object


# View as an API view
product_destroy_view = ProductDeleteAPIView.as_view()

# mixins are a type of reusable class used to add functionality to views
# They allow developers to compose views with small, reusable pieces of logic by combining multiple mixins into a single class


# list ListModelMixin used to retrieve all data, like get method
# retrieveModelMixin is used to retrieve a single data or specific data
class ProductMixins(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"

    def get(self, request, *args, **kwargs):
        print(args, kwargs)  # it print the pk the object
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


product_mixin_view = ProductMixins.as_view()


# args allows a function to accept any number of positional arguments. These arguments are passed as a tuple.
# kwargs allows a function to accept any number of keyword arguments (arguments passed as key-value pairs)
# These arguments are passed as a dictionary
# function based views
@api_view(["GET", "POST"])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method

    if method == "GET":
        if pk is not None:
            # Detail view
            obj = get_object_or_404(Product, pk=pk)  # If object doesn't exist raise 404
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
            content = serializer.validated_data.get(
                "content", title
            )  # Default content to title if not provided
            serializer.save(content=content)
            return Response(serializer.data)
        return Response({"detail": "Invalid data"})
