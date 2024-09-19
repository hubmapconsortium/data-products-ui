from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view

from .serializers import *
from data_products.models import *

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


def data_product_list(request):

    if request.method == 'GET':
        dataproducts = DataProduct.objects.all()
        serializer = DataProductSerializer(dataproducts, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DataProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def tissue_list(request):
    
    if request.method == 'GET':
        tissues = Tissue.objects.all()
        serializer = TissueSerializer(tissues, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TissueSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def dataset_list(request):

    if request.method == 'GET':
        datasets = Dataset.objects.all()
        serializer = DatasetSerializer(datasets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DatasetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def assay_list(request):
    if request.method == 'GET':
        assays = Assay.objects.all()
        serializer = AssaySerializer(assays, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AssaySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def data_product_detail(request, data_product_id):
    """
    Retrieve, update or delete a data product.
    """
    try:
        product = DataProduct.objects.get(data_product_id=data_product_id)
    except DataProduct.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = DataProductSerializer(product)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DataProductSerializer(product, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return HttpResponse(status=204)

def assay_detail(request, assayName):
    """
    Retrieve, update or delete an assay type
    """
    try:
        assay = Assay.objects.get(assayName=assayName)
    except Assay.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = AssaySerializer(assay)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = AssaySerializer(assay, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        assay.delete()
        return HttpResponse(status=204)

def tissue_detail(request, tissuetype):
    """
    Retrieve, update or delete a tissue type
    """
    try:
        tissue = Tissue.objects.get(tissuetype=tissuetype)
    except Tissue.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TissueSerializer(tissue)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = TissueSerializer(tissue, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        assay.delete()
        return HttpResponse(status=204)

def dataset_detail(request, uuid):
    """
    Retrieve, update or delete a dataset
    """
    try:
        dataset = Dataset.objects.get(uuid=uuid)
    except Dataset.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = DatasetSerializer(dataset)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DatasetSerializer(dataset, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        assay.delete()
        return HttpResponse(status=204)
