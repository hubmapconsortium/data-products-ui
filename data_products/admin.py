from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import DataProduct, Dataset, Tissue

admin.site.register(DataProduct)
admin.site.register(Dataset)
admin.site.register(Tissue)

