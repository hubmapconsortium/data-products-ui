import os

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth.models import Group, User
from django.db import connections
from django.db.utils import OperationalError
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *
from data_products.models import *


def data_product_list(request):

    if request.method == 'GET':
        dataproducts = DataProduct.objects.all()
        serializer = DataProductSerializer(dataproducts, many=True)
        return JsonResponse(serializer.data, safe=False)

def tissue_list(request):
    
    if request.method == 'GET':
        tissues = Tissue.objects.all()
        serializer = TissueSerializer(tissues, many=True)
        return JsonResponse(serializer.data, safe=False)

def dataset_list(request):

    if request.method == 'GET':
        datasets = Dataset.objects.all()
        serializer = DatasetSerializer(datasets, many=True)
        return JsonResponse(serializer.data, safe=False)


def assay_list(request):

    if request.method == 'GET':
        assays = Assay.objects.all()
        serializer = AssaySerializer(assays, many=True)
        return JsonResponse(serializer.data, safe=False)


def data_product_detail(request, data_product_id):

    try:
        product = DataProduct.objects.get(data_product_id=data_product_id)
    except DataProduct.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = DataProductSerializer(product)
        return JsonResponse(serializer.data)


def assay_detail(request, assayName):

    try:
        assay = Assay.objects.get(assayName=assayName)
    except Assay.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = AssaySerializer(assay)
        return JsonResponse(serializer.data)

def tissue_detail(request, tissuetype):

    try:
        tissue = Tissue.objects.get(tissuetype=tissuetype)
    except Tissue.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TissueSerializer(tissue)
        return JsonResponse(serializer.data)

def dataset_detail(request, uuid):

    try:
        dataset = Dataset.objects.get(uuid=uuid)
    except Dataset.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = DatasetMappingSerializer(dataset)
        return JsonResponse(serializer.data)


def status_view(request):
    try:
        connections['default'].cursor()
        mysql_connection = True
    except OperationalError:
        mysql_connection = False

    status_data = {
        "build": "main:prod",  
        "mysql_connection": mysql_connection,
        "version": "prod"
    }
    return JsonResponse(status_data)


def data_products_by_tissue(request, tissuetype):
    if request.method != 'GET':
        return HttpResponse(status=405)

    try:
        tissue = Tissue.objects.get(tissuetype__iexact=tissuetype)
        data_products = DataProduct.objects.filter(tissue=tissue)
    except Tissue.DoesNotExist:
        return HttpResponse(status=404)

    serializer = DataProductSerializer(data_products, many=True)
    return JsonResponse(serializer.data, safe=False)


def data_products_by_assay(request, assayName):
    if request.method != 'GET':
        return HttpResponse(status=405)

    try:
        assay = Assay.objects.get(assayName__iexact=assayName)
        data_products = DataProduct.objects.filter(assay=assay)
    except Assay.DoesNotExist:
        return HttpResponse(status=404)

    serializer = DataProductSerializer(data_products, many=True)
    return JsonResponse(serializer.data, safe=False)
