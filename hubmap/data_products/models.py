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
    tissuecode = models.CharField(max_length=2)

    def __repr__(self):
        return self.tissuetype

    def __str__(self):
        return "%s" % self.tissuetype


class Assay(models.Model):

    assayName = models.CharField(max_length=32)

    @classmethod
    def get_default_pk(cls):
        assay, created = cls.objects.get_or_create(
            assayName = "default"
        )
        return assay.pk

    def __repr__(self):
        return self.assayName

    def __str__(self):
        return "%s" % self.assayName


class DataProduct(models.Model):

    data_product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    creation_time = models.DateTimeField(auto_now_add=True)
    tissue = models.ForeignKey(Tissue, on_delete=models.CASCADE)

    dataSets = models.ManyToManyField(Dataset, blank=True)
    
    download = models.URLField(null=True, blank=True)
    umap_plot = models.ImageField(null=True, blank=True, upload_to="images/")
    raw_total_cell_count = models.PositiveIntegerField(null=True, blank=True)
    processed_total_cell_count = models.PositiveIntegerField(null=True, blank=True)
    processed_cell_type_counts = models.JSONField(blank=True)
    raw_cell_type_counts = models.JSONField(blank=True)
    raw_file_size_bytes = models.PositiveBigIntegerField(blank=True)
    processed_file_sizes_bytes = models.PositiveBigIntegerField(blank=True)
    assay = models.ForeignKey(Assay, on_delete=models.CASCADE, default=Assay.get_default_pk)

    #link to this data product's shiny app
    shiny_app = models.URLField(null=True, blank=True)

    def __repr__(self):
        return self.data_product_id

    def __str__(self):
        return "%s" % self.data_product_id

    # def __str__(self):
    #     datasets_str = ", ".join([str(dataset) for dataset in self.datasets.all()])
    #     return f"{self.data_product_id} (Datasets: {datasets_str})"
