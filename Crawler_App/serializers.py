from rest_framework import serializers
from .models import ProductDetails, HtmlModel
 
 
class ProductDetailsSerializer(serializers.ModelSerializer): 
    class Meta:
        model = ProductDetails
        fields = ('id',
                  'sku', 
                  'title',
                  'price',
                  'description',
                  'ratings',
                  'timestamp')


class HtmlSerializer(serializers.ModelSerializer):
    class Meta:
        model = HtmlModel
        fields = ('id',
                  'sku',
                  '_html')


class SKUSerializer(serializers.Serializer):
    """Serializes an sku field for testing out APIView"""
    sku = serializers.CharField(max_length=2000)
    

class ProductHistorySerializer(serializers.Serializer):
    """Serializes an sku and timestamp field for testing out APIView"""
    sku = serializers.CharField(max_length=2000)
    timestamp = serializers.DateTimeField()


class PriceTrendSerializer(serializers.Serializer):
    """Serializes an sku, timestamp, price fields for testing out APIView"""
    sku = serializers.CharField(max_length=2000)    
    timestamp = serializers.DateTimeField()    
    price = serializers.CharField(max_length =200)