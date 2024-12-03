from django.contrib.auth.models import Group, User
from rest_framework import serializers
from data_products.models import *
import urllib.request, json 

class TissueSerializer(serializers.Serializer):
    tissuetype = serializers.CharField(read_only=True)
    tissuecode = serializers.CharField(read_only=True)
    uberoncode= serializers.SerializerMethodField()

    def get_uberoncode(self, obj):
        tcode = obj.tissuecode
        with urllib.request.urlopen("https://ontology.api.hubmapconsortium.org/organs?application_context=HUBMAP") as url:
            data = json.load(url)
            result = [x["organ_uberon"] for x in data if x["rui_code"]==tcode]
            if result:
                return result[0]
            return None
    
class AssaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Assay
        fields = ['assayName']


class DatasetSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    hubmap_id = serializers.SerializerMethodField()
    
    def get_hubmap_id(self,obj):
        return obj.hbmid
        
    annotation_metadata = serializers.JSONField(read_only=True)

class DataProductSerializer(serializers.Serializer):
    data_product_id = serializers.UUIDField(read_only=True)
    creation_time = serializers.DateTimeField(read_only=True)
    tissue = TissueSerializer(read_only=True, many=False)
    dataSets = DatasetSerializer(read_only=True, many=True)
    assay = AssaySerializer(required=True)
    download = serializers.SerializerMethodField()

    def get_download(self, obj):
        if obj.download is not None:
            if obj.assay.assayName == "rna-seq":
                return obj.download+"/"+obj.tissue.tissuecode+"_processed.h5ad"
            elif obj.assay.assayName =="multiome-rna-atac":
                return obj.download+"/"+obj.tissue.tissuecode+"_processed.h5mu"
            else:
                return "None"
        else:
            return "None"
   
    download_raw = serializers.SerializerMethodField()

    def get_download_raw(self, obj):
        if obj.download is not None:
            if (obj.assay.assayName == "atac" or obj.assay.assayName == "multiome-rna-atac"):
                return obj.download+"/"+obj.tissue.tissuecode+".h5mu"
            else:
                return obj.download+"/"+obj.tissue.tissuecode+"_raw.h5ad"
        else:
            return "None"

    raw_file_size_bytes = serializers.IntegerField(read_only=True)
    processed_file_sizes_bytes = serializers.IntegerField(read_only=True)

    raw_cell_type_counts = serializers.JSONField(read_only=True)
    processed_cell_type_counts = serializers.JSONField(read_only=True)

class DatasetMappingSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    hubmap_id = serializers.SerializerMethodField()
    dataproduct_set = DataProductSerializer(many=True, read_only=True)
    
    def get_hubmap_id(self,obj):
        return obj.hbmid
        
    annotation_metadata = serializers.JSONField(read_only=True)
