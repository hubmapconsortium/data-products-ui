from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("admin/", admin.site.urls),
    path("data_products/", include("data_products.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
