from rest_framework import serializers
from rest_framework.serializers import FileField
from .models import XmlModel,Post,Csv,Product,ProductSearch, IdSearch
class XmlSerializer(serializers.ModelSerializer):
    class Meta:
        model = XmlModel
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
class CsvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Csv
        fields = ['field','file_name']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields = '__all__'

class ProductSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSearch
        fields = '__all__'

class IdSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdSearch
        fields = '__all__'