from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader

def index(request):

    return redirect("https://portal.hubmapconsortium.org/integrated-maps")
