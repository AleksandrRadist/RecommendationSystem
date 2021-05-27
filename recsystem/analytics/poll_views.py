from .models import Order, CommercialInfo
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .utils import get_clients_data_age, get_clients_data_gender


def order_data_gender(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    flag = request.GET.get('clients')
    if flag == 'performed_action':
        clients = order.commercial_info.performed_action_clients
    elif flag == 'shown':
        clients = order.commercial_info.shown_clients
    elif flag == 'clicked':
        clients = order.commercial_info.clicked_clients
    else:
        clients = order.clients
    data = get_clients_data_gender(clients)
    return JsonResponse(data, safe=False)


def order_data_age(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    flag = request.GET.get('clients')
    if flag == 'performed_action':
        clients = order.commercial_info.performed_action_clients
    elif flag == 'shown':
        clients = order.commercial_info.shown_clients
    elif flag == 'clicked':
        clients = order.commercial_info.clicked_clients
    else:
        clients = order.clients
    data = get_clients_data_age(clients)
    return JsonResponse(data, safe=False)