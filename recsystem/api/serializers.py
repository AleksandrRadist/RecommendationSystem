from analytics.models import Order
from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.settings import api_settings


class OrderSerializer(serializers.ModelSerializer):
    code = serializers.CharField(read_only=True)
    class Meta:
        fields = '__all__'
        model = Order


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('company_name', 'category', 'date_start', 'date_end')
        model = Order


class OrderClientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('company_name', 'category', 'date_start', 'date_end', 'clients_number', 'transactions_number', 'price', 'days',)
        model = Order
