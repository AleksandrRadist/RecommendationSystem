from analytics.models import Order
from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.settings import api_settings


class OrderSerializer(serializers.ModelSerializer):
    code = serializers.CharField(read_only=True)
    transactions_number = serializers.IntegerField(read_only=True)
    clients_number = serializers.IntegerField(read_only=True)
    price = serializers.FloatField(read_only=True)
    days = serializers.IntegerField(read_only=True)
    clients = serializers.JSONField(read_only=True)
    status = serializers.BooleanField(read_only=True)
    date_start = serializers.DateField(required=True)
    date_end = serializers.DateField(required=True)
    company_name = serializers.CharField(required=True)

    class Meta:
        fields = '__all__'
        model = Order


class OrderPublicSerializer(serializers.ModelSerializer):
    code = serializers.CharField(read_only=True)
    transactions_number = serializers.IntegerField(read_only=True)
    clients_number = serializers.IntegerField(read_only=True)
    price = serializers.FloatField(read_only=True)
    days = serializers.IntegerField(read_only=True)
    status = serializers.BooleanField(read_only=True)
    date_start = serializers.DateField(required=True)
    date_end = serializers.DateField(required=True)
    company_name = serializers.CharField(required=True)

    class Meta:
        fields = ('company_name', 'category', 'date_start', 'date_end', 'clients_number', 'transactions_number', 'price', 'days', 'status', 'code')
        model = Order
