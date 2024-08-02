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


def register_data_product(metadata_file, umap_file):
    metadata = read_metadata(metadata_file)
    data_product_uuid = metadata["Data Product UUID"]
    tissue_type = metadata["Tissue"]
    dataset_uuids = metadata["Dataset UUIDs"]
    dataset_hbmids = metadata["Dataset HBMIDs"]
    dataset_list = register_datasets(dataset_uuids, dataset_hbmids)
    raw_cell_count = metadata["Raw Total Cell Count"]
    processed_cell_count = metadata["Processed Total Cell Count"]
    directory_url = f"https://hubmap-data-products.s3.amazonaws.com/{data_product_uuid}"
    shiny_url = f"https://data-products.cmu.hubmapconsortium.org/shiny/{data_product_uuid}"
    raw_cell_types_counts = metadata["Raw Cell Type Counts"]
    processed_cell_types_counts = metadata["Processed Cell Type Counts"]    
    data_product = DataProduct.objects.get_or_create(
        data_product_id = data_product_uuid,
        tissue = register_tissue(tissue_type),
        download = directory_url,
        umap_plot = umap_file ,
        raw_total_cell_count = raw_cell_count,
        processed_total_cell_count = processed_cell_count,
        shiny_app = shiny_url,
        raw_cell_type_counts = raw_cell_types_counts,
        processed_cell_type_counts = processed_cell_types_counts
    )[0]

    for dataset in dataset_list:
        dataset.data_product = data_product
        dataset.save()
    
    data_product.save()


def register_data_products(metadata_list, umap_list):
    for metadata, umap in zip(metadata_list, umap_list):
        register_data_product(metadata, umap)


def read_metadata(metadata_file):
    with open(metadata_file, 'r') as json_file:
        metadata = json.load(json_file)
    return metadata


def find_metadatas(directory):
    pattern = re.compile(r'.*\.json$')
    metadatas = find_files(directory, pattern)
    return metadatas


def find_umaps(metadatas, directory):
    umap_pngs = []
    for file_path in metadatas:
        filename = os.path.basename(file_path)
        file = os.path.splitext(filename)
        png = f"{file[0]}.png"
        umap_pngs.append(os.path.join(directory, png))
    return umap_pngs   


def copy_umaps(umap_paths):
    new_umap_paths = []
    for umap in umap_paths:
        filename = os.path.basename(umap)
        file = os.path.splitext(filename)
        png = f"{file[0]}.png"
        shutil.copy(umap, f"/media/{png}")
        new_umap_path = png
        new_umap_paths.append(new_umap_path)
    return new_umap_paths


def find_files(directory, pattern):
    json_files = []
    for root, dirs, files, in os.walk(directory):
        for filename in files:
            if pattern.match(filename):
                json_files.append(os.path.join(root, filename))
    return json_files


def delete_json_file(directory, json_file):
    try: 
        os.remove(os.path.join(directory, json_file))
        print(f"Deleted: {json_file}")
    except Exception as e:
        print(f"Error deleting file {json_file}: {e}")


def main(directory):
    metadata_files = find_metadatas(directory)
    umap_files = find_umaps(metadata_files, directory)
    updated_umap_files = copy_umaps(umap_files)
    register_data_products(metadata_files, updated_umap_files)
    for file in metadata_files:
        delete_json_file(directory, file)


if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument("directory", type=Path)
    args = p.parse_args()

    main(args.directory)
