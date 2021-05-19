import uuid
from django.contrib.auth.tokens import default_token_generator
from analytics.models import Order, Category, Transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import (OrderSerializer, OrderPublicSerializer)


@api_view(['GET'])
def api_orders_detail(request, code):
    if request.user.is_authenticated:
        order = get_object_or_404(Order, code=code)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def api_orders_public_detail(request, code):
    order = get_object_or_404(Order, code=code)
    serializer = OrderPublicSerializer(order)
    return Response(serializer.data)


@api_view(['POST'])
def api_orders_status_update(request, code):
    order = get_object_or_404(Order, code=code)
    order.status = not order.status
    order.save()
    serializer = OrderPublicSerializer(order)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', "GET"])
def api_orders(request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_403_FORBIDDEN)
    if request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            category = Category.objects.get(name=serializer.validated_data['category'])
            transactions = Transaction.objects.filter(product_category=category.id)
            transactions_number = transactions.count()
            clients = []
            for i in transactions.values('client_id').distinct():
                clients.append(i['client_id'])
            clients = clients
            clients_number = len(clients)
            delta = serializer.validated_data['date_end'] - serializer.validated_data['date_start']
            days = delta.days + 1
            price = (days // 7 + 1) * 20 * clients_number
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


@api_view(['POST'])
def api_orders_public(request):
    if request.method == 'POST':
        serializer = OrderPublicSerializer(data=request.data)
        if serializer.is_valid():
            category = Category.objects.get(name=serializer.validated_data['category'])
            transactions = Transaction.objects.filter(product_category=category.id)
            transactions_number = transactions.count()
            clients = []
            for i in transactions.values('client_id').distinct():
                clients.append(i['client_id'])
            clients = clients
            clients_number = len(clients)
            delta = serializer.validated_data['date_end'] - serializer.validated_data['date_start']
            days = delta.days + 1
            price = (days // 7 + 1) * 20 * clients_number
            code = uuid.uuid4().hex[:10].upper()
            serializer.save(transactions_number=transactions_number,
                            clients=clients,
                            clients_number=clients_number,
                            price=price,
                            days=days,
                            code=code)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
