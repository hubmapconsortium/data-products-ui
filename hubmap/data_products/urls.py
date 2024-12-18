from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<uuid:data_product_id>/", views.detail, name="detail"),
    path("<str:tissuetype>/", views.tissue, name="tissue"),
    path("latest/<str:tissuecode>/<str:assayName>", views.detail_latest),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
