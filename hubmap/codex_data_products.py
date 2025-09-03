if __name__ == "__main__":
    import django
    django.setup()

import json
import re
import os
import pandas as pd
import shutil
import yaml
from data_products.models import DataProduct, Tissue, Assay, Dataset
from argparse import ArgumentParser
from pathlib import Path

#organ_types_yaml = Path("organ_types.yaml")


def register_assay():
    assay = Assay.objects.get_or_create(assayName="codex")[0]
    assay.save()
    return assay


def get_tissue(tissue_yaml, tissue):
    with open(tissue_yaml, 'r') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    tissue_name = data.get(tissue)['description']
    return tissue_name


def register_datasets(uuids, hbmids):
    datasets = []
    for dataset_uuid, dataset_hbmid in zip(uuids, hbmids):
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


def register_data_product(metadata_file):
    metadata = read_metadata(metadata_file)
    data_product_uuid = metadata["Data Product UUID"]
    tissue_type = metadata["Tissue"]
    dataset_uuids = metadata["Dataset UUIDs"]
    dataset_hbmids = metadata["Dataset HBMIDs"]
    dataset_list = register_datasets(dataset_uuids, dataset_hbmids)
    raw_cell_count = metadata["Total Cell Count"]
    directory_url = f"https://g-24f5cc.09193a.5898.dn.glob.us/public/hubmap-data-products/{data_product_uuid}"
    raw_file_size = metadata["Raw File Size"]
    data_product = DataProduct.objects.get_or_create(
        data_product_id = data_product_uuid,
        tissue = register_tissue(tissue_type),
        download = directory_url,
        raw_total_cell_count = raw_cell_count,
        processed_total_cell_count = 0,
        raw_cell_type_counts = {},
        processed_cell_type_counts = {},
        processed_file_sizes_bytes = 0,
        raw_file_size_bytes = raw_file_size,
        assay = register_assay()
    )[0]
    data_product.save()
    data_product.dataSets.add(*dataset_list)
    data_product.save()


def register_data_products(metadata_list):
    for metadata in metadata_list:
        register_data_product(metadata)


def read_metadata(metadata_file):
    with open(metadata_file, 'r') as json_file:
        metadata = json.load(json_file)
    return metadata


def find_metadatas(directory):
    pattern = re.compile(r'.*\.json$')
    metadatas = find_files(directory, pattern)
    return metadatas


def find_files(directory, pattern):
    json_files = []
    for root, dirs, files, in os.walk(directory):
        for filename in files:
            if pattern.match(filename):
                json_files.append(os.path.join(root, filename))
    return json_files


def delete_json_file(json_file):
    try: 
        os.remove(json_file)
        print(f"Deleted: {json_file}")
    except Exception as e:
        print(f"Error deleting file {json_file}: {e}")


def main(directory):
    metadata_files = find_metadatas(directory)
    register_data_products(metadata_files)
    for file in metadata_files:
        delete_json_file(file)


if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument("directory", type=Path)
    args = p.parse_args()

    main(args.directory)
