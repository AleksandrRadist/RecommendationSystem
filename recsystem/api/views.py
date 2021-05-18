from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from analytics.models import Order, Category, Transaction
from .serializers import (OrderSerializer, OrderClientSerializer, OrderCreateSerializer)
import uuid


@api_view(['POST', "GET"])
def api_orders(request):
    if request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            category_id = Category.objects.filter(name=serializer.validated_data['category'])
            transactions = Transaction.objects.filter(product_category__in=category_id)
            transactions_number = transactions.count()
            clients = []
            for i in transactions.values('client_id').distinct():
                clients.append(i['client_id'])
            clients = clients
            clients_number = len(clients)
            delta = serializer.validated_data['date_end'] - serializer.validated_data['date_start']
            days = delta.days + 1
            price = days // 7 + 1 * 20 * clients_number
            code = uuid.uuid4().hex[:10].upper()
            serializer.save(transactions_number=transactions_number,
                            clients=clients,
                            clients_number=clients_number,
                            price=price,
                            days=days,
                            code=code)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        orders = Order.objects.filter(status=True)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def api_orders_client(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'GET':
        serializer = OrderClientSerializer(order)
        return Response(serializer.data)


@api_view(['GET'])
def api_orders_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'GET':
        serializer = OrderSerializer(order)
        return Response(serializer.data)
