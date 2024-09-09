# Generated by Django 4.2.11 on 2024-09-02 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data_products", "0008_alter_dataproduct_processed_file_sizes_bytes_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="dataset",
            name="data_product",
        ),
        migrations.AlterField(
            model_name="dataproduct",
            name="processed_file_sizes_bytes",
            field=models.PositiveBigIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name="dataproduct",
            name="raw_file_size_bytes",
            field=models.PositiveBigIntegerField(blank=True, default=0, null=True),
        ),
    ]