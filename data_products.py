if __name__ == "__main__":
    import django
    django.setup()

import anndata as ad
import s3fs
import h5py
import pandas as pd
import yaml
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


def open_h5ad_file(access_key_id, secret_access_key, url):
    s3 = s3fs.S3FileSystem(key = access_key_id, secret = secret_access_key)
    with s3.open(url, 'rb') as f:
        h5ad = ad.read_h5ad(f)
        f.close()
    return h5ad


def open_umap(access_key_id, secret_access_key, url):
    s3 = s3fs.S3FileSystem(key = access_key_id, secret = secret_access_key)
    f = s3.open(url)
    return f


def get_datasets(access_key_id, secret_access_key, url):
    h5ad = open_h5ad_file(access_key_id, secret_access_key, url)
    uuids = h5ad.obs["dataset"].drop_duplicates()
    hbmids = h5ad.obs["hubmap_id"].drop_duplicates()
    dataset_ids = uuids.to_frame().join(hbmids)
    return dataset_ids


def register_datasets(dataset_ids: pd.DataFrame):
    datasets = []
    for index, row in dataset_ids.iterrows():
        dataset_uuid = row['dataset']
        dataset_hbmid = row['hubmap_id']
        dataset = Dataset.objects.get_or_create(
            uuid = dataset_uuid,
            hbmid = dataset_hbmid
        )[0]
        dataset.save()
        datasets.append(dataset)
    return datasets


def register_tissue(tissue_type):
    tissue = Tissue.objects.get_or_create(tissuetype = tissue_type)[0]
    tissue.save()
    return tissue


def register_data_product(data_product, dataset_list, umap, tissue_type):
    data_product = DataProduct.objects.get_or_create(
        tissue = register_tissue(tissue_type),
        datasets = dataset_list,
        download = data_product,
        umap_plot = umap
    )[0]
    data_product.save()


def main(tissue_key, access_key_id, secret_access_key):
    bucket = f"s3://hubmap-data-products/{tissue_key}/"
    processed_file = f"{tissue_key}_processed.h5ad"
    raw_file = f"{tissue_key}_raw.h5ad"
    umap_file = f"{tissue_key}.png"
    data_product_file_names = [processed_file, raw_file]
    processed_url = bucket+processed_file
    raw_url = bucket+raw_file
    umap_url = bucket+umap_file
    data_product_urls = [processed_url, raw_url]
    tissue_type = get_tissue_type(tissue_key)
    dataset_ids = get_datasets(access_key_id, secret_access_key, raw_url)
    # processed_file = open_h5ad_file(access_key_id, secret_access_key, processed_url)
    # raw_file = open_h5ad_file(access_key_id, secret_access_key, raw_url)
    umap = open_umap(access_key_id, secret_access_key, umap_url)
    # # h5ads = [processed_file, raw_file]
    datasets = register_datasets(dataset_ids)
    for data_product in data_product_urls:
        register_data_product(data_product, datasets, umap, tissue_type)


if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument("tissue", type=str)
    p.add_argument("access_key_id", type=str)
    p.add_argument("secret_access_key", type=str)
    
    args = p.parse_args()

    main(args.tissue, args.access_key_id, args.secret_access_key)
