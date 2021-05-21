from analytics.models import Order, Message
from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.settings import api_settings


class OrderWriteSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    date_start = serializers.DateField(required=True)
    date_end = serializers.DateField(required=True)
    company_name = serializers.CharField(required=True)

    class Meta:
        fields = ('company_name', 'email', 'date_start', 'date_end', 'category',)
        model = Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Order


class OrderPublicSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'company_name', 'category', 'date_start', 'date_end', 'clients_number',
            'transactions_number', 'price', 'days', 'confirmation_status', 'code',
            'email', 'completion_status', 'acceptance_status',
        )
        model = Order


class MessageSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(read_only=True)
    read_status = serializers.BooleanField(read_only=True)

    class Meta:
        fields = ('text', 'creation_date', 'read_status', 'email')
        model = Message
