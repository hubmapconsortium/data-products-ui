import json
import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models

EXPIRATION_TIME = 14400  # 4 hours in seconds


def annotation_default():
    return {"is_annotated": False}


def summary_default():
    return {}

class Dataset(models.Model):

    uuid = models.CharField(max_length=32)
    hbmid = models.CharField(max_length=16)

    annotation_metadata = models.JSONField(default=annotation_default)

    def __repr__(self):
        return self.uuid

    def __str__(self):
        return "%s" % self.uuid


class Tissue(models.Model):

    tissuetype = models.CharField(max_length=32)

    def __repr__(self):
        return self.tissuetype

    def __str__(self):
        return "%s" % self.tissuetype

class Assay(models.Model):

    assayName = models.CharField(max_length=32)

    def __repr__(self):
        return self.assayName

    def __str__(self):
        return "%s" % self.assayName

class DataProduct(models.Model):

    data_product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    creation_time = models.DateTimeField(auto_now_add=True)
    tissue = models.ForeignKey(Tissue, on_delete=models.CASCADE)
    datasets = models.ManyToManyField(Dataset)
    download = models.URLField(null=True, blank=True)
    umap_plot = models.ImageField(null=True, blank=True, upload_to="images/")
    raw_total_cell_count = models.IntegerField(null=True, blank=True)
    processed_total_cell_count = models.IntegerField(null=True, blank=True)
    # cell type count

    shinyApp = models.URLField(null=True, blank=True)

    def __repr__(self):
        return self.dataProductId

    def __str__(self):
        return "%s" % self.dataProductId

