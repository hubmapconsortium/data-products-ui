from django.contrib.auth.models import Group, User
from rest_framework import serializers
from data_products.models import *

class TissueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tissue
        fields = ['tissuetype', 'tissuecode']
    
class AssaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Assay
        fields = ['assayName']

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ['uuid', 'hbmid', 'annotation_metadata']

class DataProductSerializer(serializers.Serializer):
    data_product_id = serializers.UUIDField(read_only=True)
    creation_time = serializers.DateTimeField(read_only=True)
    tissue = TissueSerializer(read_only=True, many=False)
    dataSets = DatasetSerializer(read_only=True, many=True)
    assay = AssaySerializer(required=True)
    download = serializers.SerializerMethodField()

    def get_download(self, obj):
        return obj.download+"/"+obj.tissue.tissuecode+"_processed.h5ad"
   

    download_raw = serializers.SerializerMethodField()

    def get_download_raw(self, obj):
        return obj.download+"/"+obj.tissue.tissuecode+"_raw.h5ad"

    raw_file_size_bytes = serializers.IntegerField(read_only=True)
    processed_file_sizes_bytes = serializers.IntegerField(read_only=True)
