# Generated by Django 4.2.14 on 2024-07-19 12:53

import uuid

import django.db.models.deletion
from django.db import migrations, models

import data_products.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Assay",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("assayName", models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name="DataProduct",
            fields=[
                (
                    "data_product_id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("creation_time", models.DateTimeField(auto_now_add=True)),
                ("download", models.URLField(blank=True, null=True)),
                ("umap_plot", models.ImageField(blank=True, null=True, upload_to="images/")),
                ("raw_total_cell_count", models.IntegerField(blank=True, null=True)),
                ("processed_total_cell_count", models.IntegerField(blank=True, null=True)),
                ("shiny_app", models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Tissue",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("tissuetype", models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name="Dataset",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("uuid", models.CharField(max_length=32)),
                ("hbmid", models.CharField(max_length=16)),
                (
                    "annotation_metadata",
                    models.JSONField(default=data_products.models.annotation_default),
                ),
                (
                    "data_product",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="datasets",
                        to="data_products.dataproduct",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="dataproduct",
            name="tissue",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="data_products.tissue"
            ),
        ),
    ]
