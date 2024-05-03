from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader

from .models import DataProduct

def index(request):
    latest_data_product_list = DataProduct.objects.order_by("creation_time")[:5]
    template = loader.get_template("data_products/index.html")
    context = {
        "latest_data_product_list": latest_data_product_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, dataProductId):
    #return HttpResponse("You're looking at dataProduct %s." % dataProductId)

    product = get_object_or_404(DataProduct, pk=dataProductId)
    return render(request, "data_products/detail.html", {"product": product})
