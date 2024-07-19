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

    dataProductId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    creation_time = models.DateTimeField(auto_now_add=True)
    tissue = models.ForeignKey(Tissue, on_delete=models.CASCADE)
    datasets = models.ManyToManyField(Dataset)
    download = models.FileField(null=True, blank=True, upload_to="uploads/")
    umap_plot = models.ImageField(null=True, blank=True, upload_to="images/")

    number_cells = models.IntegerField(default=0)
    number_cell_types = models.IntegerField(default=0)

    shinyApp = models.URLField(null=True, blank=True)

    def __repr__(self):
        return self.dataProductId

    def __str__(self):
        return "%s" % self.dataProductId

