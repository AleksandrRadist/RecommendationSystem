import uuid
import datetime
from analytics.models import Order, Category, Transaction, Message
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import (OrderSerializer, OrderPublicSerializer, OrderWriteSerializer, MessageSerializer,
                          MessagePublicSerializer, MessageWriteSerializer)


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
def api_orders_confirm(request, code):
    order = get_object_or_404(Order, code=code)
    order.confirmation_status = True
    order.save()
    serializer = OrderPublicSerializer(order)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def api_orders_cancel(request, code):
    order = get_object_or_404(Order, code=code)
    if order.completion_status or order.acceptance_status:
        return Response(status=status.HTTP_409_CONFLICT)
    order.confirmation_status = False
    order.save()
    serializer = OrderPublicSerializer(order)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', "GET"])
def api_orders(request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_403_FORBIDDEN)
    if request.method == 'POST':
        serializer = OrderWriteSerializer(data=request.data)
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
            order = Order.objects.get(code=code)
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def api_orders_confirmed(request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_403_FORBIDDEN)
    orders = Order.objects.filter(confirmation_status=True, acceptance_status=False)
    serializer = OrderSerializer(orders)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def api_orders_unconfirmed(request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_403_FORBIDDEN)
    orders = Order.objects.filter(confirmation_status=False)
    serializer = OrderSerializer(orders)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def api_orders_accepted(request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_403_FORBIDDEN)
    orders = Order.objects.filter(acceptance_status=True, completion_status=False)
    serializer = OrderSerializer(orders)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def api_orders_completed(request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_403_FORBIDDEN)
    orders = Order.objects.filter(completion_status=True)
    serializer = OrderSerializer(orders)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def api_orders_public(request):
    if request.method == 'POST':
        serializer = OrderWriteSerializer(data=request.data)
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
            order = Order.objects.get(code=code)
            return Response(OrderPublicSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def api_orders_complete(request, order_id):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_403_FORBIDDEN)
    order = get_object_or_404(Order, id=order_id)
    if not order.confirmation_status or not order.acceptance_status:
        return Response(status=status.HTTP_409_CONFLICT)
    if order.completion_status:
        return Response(status=status.HTTP_208_ALREADY_REPORTED)
    order.completion_status = True
    order.completion_date = datetime.datetime.now()
    order.save()
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def api_orders_accept(request, order_id):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_403_FORBIDDEN)
    order = get_object_or_404(Order, id=order_id)
    if not order.confirmation_status:
        return Response(status=status.HTTP_409_CONFLICT)
    if order.acceptance_status or order.completion_status:
        return Response(status=status.HTTP_208_ALREADY_REPORTED)
    order.acceptance_status = True
    order.completion_acceptance = datetime.datetime.now()
    order.save()
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', "GET"])
def api_messages(request):
    if request.method == 'POST':
        serializer = MessageWriteSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save()
            return Response(MessagePublicSerializer(message).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_403_FORBIDDEN)
    messages = Message.objects.all()
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def api_messages_read(request, message_id):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_403_FORBIDDEN)
    message = get_object_or_404(Message, id=message_id)
    message.read_status = True
    message.save()
    serializer = MessageSerializer(message)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def api_messages_read_all(request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_403_FORBIDDEN)
    messages = Message.objects.all()
    messages.update(read_status=True)
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def api_messages_new(request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_403_FORBIDDEN)
    messages = Message.objects.filter(read_status=False)
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def api_messages_red(request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_403_FORBIDDEN)
    messages = Message.objects.filter(read_status=True)
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)
