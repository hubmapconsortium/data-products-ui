from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from . import views

urlpatterns = [
    path("", views.data_product_list),
    path("data_products/", views.data_product_list),
    path("tissues", views.tissue_list),
    path("datasets", views.dataset_list),
    path("assays", views.assay_list),
    path("data_products/<uuid:data_product_id>/", views.data_product_detail),
    path("assays/<str:assayName>/", views.assay_detail),
    path("tissues/<str:tissuetype>/", views.tissue_detail),
    path("datasets/<str:uuid>/", views.dataset_detail),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
