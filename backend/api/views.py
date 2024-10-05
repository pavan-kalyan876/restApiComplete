from django.shortcuts import render
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json
from products.models import Product
from products.serializers import ProductSerializer

# Create your views here.


@api_view(["POST"])
def api_home(request, *args, **kwargs):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        print(instance)
        

    # instance = Product.objects.all().order_by("?").first()
    # data = {}
    # if instance:

    #     data = ProductSerializer(instance).data
    return Response(serializer.data)
