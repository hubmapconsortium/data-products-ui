from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView
#from rest_framework import routers

from . import views

#router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
#router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path("", views.index, name="index"),
    path("admin/", admin.site.urls),
    path("data_products/", RedirectView.as_view(url="https://portal.hubmapconsortium.org/integrated-maps", permanent=True)),
    path("api/", include("api.urls")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
