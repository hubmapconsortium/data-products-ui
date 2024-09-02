# Register your models here.
from django.contrib import admin

from .models import DataProduct, Dataset, Tissue, Assay

admin.site.register(DataProduct)
admin.site.register(Dataset)
admin.site.register(Tissue)
admin.site.register(Assay)
