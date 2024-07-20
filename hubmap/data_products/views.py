from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader

from .models import DataProduct, Tissue


def index(request):
    tissue_list = Tissue.objects.order_by("tissuetype")
    latest_data_product_list=[]
    for t in tissue_list:
        latest_data_product_t=DataProduct.objects.filter(tissue=t).order_by("-creation_time")
        latest_data_product_list.append(latest_data_product_t[0])
    template = loader.get_template("data_products/index.html")
    context = {
        "latest_data_product_list": latest_data_product_list,
    }
    return HttpResponse(template.render(context, request))


def detail(request, data_product_id):
    # return HttpResponse("You're looking at dataProduct %s." % dataProductId)

    product = get_object_or_404(DataProduct, pk=data_product_id)
    return render(request, "data_products/detail.html", {"product": product})

def tissue(request, tissuetype):

    tissue = Tissue.objects.filter(tissuetype=tissuetype)
    tissue_data_product_list = DataProduct.objects.filter(tissue__in=tissue.all()).order_by("-creation_time")
    template = loader.get_template("data_products/index.html")
    context = {
        "latest_data_product_list": tissue_data_product_list,
    }
    return HttpResponse(template.render(context, request))
