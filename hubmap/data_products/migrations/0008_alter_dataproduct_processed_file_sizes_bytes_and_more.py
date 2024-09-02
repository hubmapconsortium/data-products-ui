# Generated by Django 4.2.11 on 2024-08-31 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data_products", "0007_dataproduct_datasets"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dataproduct",
            name="processed_file_sizes_bytes",
            field=models.PositiveBigIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name="dataproduct",
            name="raw_file_size_bytes",
            field=models.PositiveBigIntegerField(blank=True, default=0),
        ),
    ]
