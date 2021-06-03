from analytics.models import Order, Message, CommercialInfo, Client
from rest_framework import serializers
import datetime


class OrderWriteSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    date_start = serializers.DateField(required=True)
    date_end = serializers.DateField(required=True)
    company_name = serializers.CharField(required=True)

    class Meta:
        fields = ('company_name', 'email', 'date_start', 'date_end', 'category',)
        model = Order

    def validate(self, data):
        deadline = datetime.datetime.today() + datetime.timedelta(days=10)
        date_start = data.get('date_start')
        date_end = data.get('date_end')
        if date_start < deadline or date_end < deadline:
            raise serializers.ValidationError(
                'Работа рекламы не может начаться ранее чем через 10 дней после создания заказа'
            )
        if date_start < date_end:
            raise serializers.ValidationError('Конечная дата не может быть раньше начальной даты')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Order


class OrderPublicSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'company_name', 'category', 'date_start', 'date_end', 'clients_number',
            'price', 'days', 'confirmation_status', 'code',
            'email', 'completion_status', 'acceptance_status',
        )
        model = Order


class MessageWriteSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        fields = ('text', 'email')
        model = Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Message


class MessagePublicSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('text', 'email')
        model = Message


class CommercialInfoPublicSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('shown_number', 'clicked_number', 'performed_action_number',)
        model = CommercialInfo


class CommercialInfoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('shown_number', 'clicked_number', 'performed_action_number',
                  'shown_clients', 'clicked_clients', 'performed_action_clients',)
        model = CommercialInfo
