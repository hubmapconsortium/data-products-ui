if __name__ == "__main__":
    import django
    django.setup()

import uuid
import s3fs
import h5py
import yaml
from datetime import datetime
from data_products.models import DataProduct, Tissue, Assay, Dataset
from argparse import ArgumentParser

organ_types_file = "organ_types.yaml"


def get_tissue_type(tissue_key):
    organ_dict = yaml.load(open((organ_types_file)), Loader=yaml.BaseLoader)
    for key in organ_dict:
        organ_dict[key] = organ_dict[key]["description"]
    if tissue_key not in organ_dict.keys():
        print(f"Tissue {tissue_key} not found")
        tissue_type = None
    else: 
        tissue_type = organ_dict[tissue_key]
    return tissue_type


# def open_h5ad_file(access_key_id, secret_access_key, url):
#     s3 = s3fs.S3FileSystem(key = access_key_id, secret = secret_access_key)
#     file = h5py.File(s3.open(url), "w")
#     return file


def open_umap(access_key_id, secret_access_key, url):
    s3 = s3fs.S3FileSystem(key = access_key_id, secret = secret_access_key)
    umap = s3.open(url)
    return umap


# def get_datasets():
#     pass


# def register_datasets(datasets):
#     for dataset in datasets:
#         dataset = Dataset.objects.get_or_create(
#         )[0]
#     dataset.save()


def register_tissue(tissue_type):
    tissue = Tissue.objects.get_or_create(tissuetype = tissue_type)[0]
    tissue.save()
    return tissue


def register_data_product(data_product, umap_url, tissue_type):
    data_product = DataProduct.objects.get_or_create(
        tissue = register_tissue(tissue_type),
        download = data_product,
        umap_plot = umap_url.close()
    )[0]
    data_product.save()


def main(tissue_key, access_key_id, secret_access_key):
    processed_url = f"s3://hubmap-data-products/{tissue_key}/{tissue_key}_processed.h5ad"
    raw_url = f"s3://hubmap-data-products/{tissue_key}/{tissue_key}_raw.h5ad"
    umap_url = f"s3://hubmap-data-products/{tissue_key}/{tissue_key}.png"
    data_product_urls = [processed_url, raw_url]
    tissue_type = get_tissue_type(tissue_key)
    # processed_file = open_h5ad_file(access_key_id, secret_access_key, processed_url)
    # raw_file = open_h5ad_file(access_key_id, secret_access_key, raw_url)
    umap = open_umap(access_key_id, secret_access_key, umap_url)
    # h5ads = [processed_file, raw_file]
    # register_datasets(dataset_urls)
    for data_product in data_product_urls:
        register_data_product(data_product, umap, tissue_type)


if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument("tissue", type=str)
    p.add_argument("access_key_id", type=str)
    p.add_argument("secret_access_key", type=str)
    
    args = p.parse_args()

    main(args.tissue, args.access_key_id, args.secret_access_key)
