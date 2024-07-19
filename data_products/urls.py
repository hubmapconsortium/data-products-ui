from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<uuid:dataProductId>/", views.detail, name="detail"),
    path("<str:tissuetype>/", views.tissue, name="tissue") 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
