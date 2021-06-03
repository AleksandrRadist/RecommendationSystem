import uuid
import datetime
from analytics.models import Order, Category, Transaction, Message, CommercialInfo
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from analytics.utils import commercial_fake_forecast_info, get_recommendation_model_data
from .serializers import (OrderSerializer, OrderPublicSerializer, OrderWriteSerializer, MessageSerializer,
                          MessagePublicSerializer, MessageWriteSerializer, CommercialInfoPublicSerializer,
                          CommercialInfoSerializer)


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
            delta = serializer.validated_data['date_end'] - serializer.validated_data['date_start']
            days = delta.days + 1
            code = uuid.uuid4().hex[:10].upper()
            serializer.save(days=days,
                            code=code)
            order = Order.objects.get(code=code)
            data = get_recommendation_model_data('version1')
            clients = []
            if data.filter(category=category).exists():
                clients = data.get(category=category).clients
            for i in clients.all():
                order.clients.add(i)
            order.clients_number = order.clients.count()
            order.price = (days // 7 + 1) * 20 * order.clients_number
            forecast_data = commercial_fake_forecast_info(order)
            order.forecast_conversion_rate = forecast_data['conversion_rate']
            order.forecast_click_through_rate = forecast_data['click_through_rate']
            order.forecast_cost_per_action = forecast_data['cpa']
            order.forecast_cost_per_click = forecast_data['cpc']
            order.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        order_filter = request.GET.get('filter', 'All')
        if order_filter == 'unconfirmed':
            orders = Order.objects.order_by('-creation_date').filter(confirmation_status=False)
        elif order_filter == 'confirmed':
            orders = Order.objects.filter(confirmation_status=True, acceptance_status=False).order_by('-creation_date')
        elif order_filter == 'accepted':
            orders = Order.objects.filter(acceptance_status=True, completion_status=False).order_by('-acceptance_date')
        elif order_filter == 'completed':
            orders = Order.objects.filter(completion_status=True).order_by('-completion_date')
        else:
            orders = Order.objects.order_by('-creation_date').all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def api_orders_public(request):
    if request.method == 'POST':
        serializer = OrderWriteSerializer(data=request.data)
        if serializer.is_valid():
            category = Category.objects.get(name=serializer.validated_data['category'])
            delta = serializer.validated_data['date_end'] - serializer.validated_data['date_start']
            days = delta.days + 1
            code = uuid.uuid4().hex[:10].upper()
            serializer.save(days=days,
                            code=code)
            order = Order.objects.get(code=code)
            data = get_recommendation_model_data('version1')
            clients = []
            if data.filter(category=category).exists():
                clients = data.get(category=category).clients
            for i in clients.all():
                order.clients.add(i)
            order.clients_number = order.clients.count()
            order.price = (days // 7 + 1) * 20 * order.clients_number
            forecast_data = commercial_fake_forecast_info(order)
            order.forecast_conversion_rate = forecast_data['conversion_rate']
            order.forecast_click_through_rate = forecast_data['click_through_rate']
            order.forecast_cost_per_action = forecast_data['cpa']
            order.forecast_cost_per_click = forecast_data['cpc']
            order.save()
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
    message_filter = request.GET.get('filter', 'All')
    if message_filter == 'new':
        messages = Message.objects.filter(read_status=False).order_by('-creation_date')
    elif message_filter == 'read':
        messages = Message.objects.filter(read_status=True).order_by('-creation_date')
    else:
        messages = Message.objects.order_by('-creation_date')
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


@api_view(['GET'])
def api_orders_public_commercial_info(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.completion_status:
        info = CommercialInfo.objects.get(order=order)
        serializer = CommercialInfoPublicSerializer(info)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_409_CONFLICT)


@api_view(['GET'])
def api_orders_commercial_info(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.completion_status:
        info = CommercialInfo.objects.get(order=order)
        serializer = CommercialInfoSerializer(info)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_409_CONFLICT)