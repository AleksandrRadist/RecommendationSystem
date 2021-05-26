from .models import Order
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .utils import get_clients_data_age, get_clients_data_gender


def order_data_gender(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    data = get_clients_data_gender(order)
    return JsonResponse(data, safe=False)


def order_data_age(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    data = get_clients_data_age(order)
    return JsonResponse(data, safe=False)