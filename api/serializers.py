from rest_framework import serializers
from products.models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = OrderProduct
        fields = '__all__'
        read_only_fields = ['id', 'total', 'created_at', 'updated_at']


class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'total', 'order_products', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'total', 'order_products', 'status', 'created_at', 'updated_at']