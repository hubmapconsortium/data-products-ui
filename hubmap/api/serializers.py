from django.contrib.auth.models import Group, User
from rest_framework import serializers
from data_products.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

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
    tissue = serializers.CharField(allow_blank=True)
    dataSets = DatasetSerializer(read_only=True, many=True)
    assay = serializers.CharField(required=True)
   
