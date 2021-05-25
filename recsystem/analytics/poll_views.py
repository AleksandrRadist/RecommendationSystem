from django.shortcuts import redirect, render
from .models import Client, Category, Transaction, Subscription, Order, Message
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Count
import datetime


def order_data_gender(request, order_id):
    data = []
    order = get_object_or_404(Order, id=order_id)
    clients = Client.objects.filter(id__in=order.clients).values('gender').annotate(count=Count('gender'))
    for i in clients:
        data.append({i['gender']: i['count']})
    return JsonResponse(data, safe=False)


def order_data_age(request, order_id):
    data = {}
    order = get_object_or_404(Order, id=order_id)
    clients = Client.objects.all().filter(id__in=order.clients).values('birthdate').annotate(count=Count('birthdate'))
    for i in clients:
        today = datetime.date.today()
        age = today.year - i['birthdate'].year - ((today.month, today.day) < (i['birthdate'].month, i['birthdate'].day))
        if age in data:
            data[age] += 1
        else:
            data[age] = 1
    result = []
    for i in data.keys():
        result.append({int(i): data[i]})
    return JsonResponse(result, safe=False)