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

def change_dataset_mapping():
    datasets = Dataset.objects.order_by("hbmid")
    for ds in datasets:
        data_prod = ds.data_product
        data_prod.dataSets.add(ds)

def main():
    if reset:
        reset_sizes()
    change_dataset_mapping()

if __name__ == "__main__":

    main()
