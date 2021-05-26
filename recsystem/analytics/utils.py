from .models import Client
from django.db.models import Count
import datetime


def get_clients_data_gender(order):
    data = []
    clients = Client.objects.filter(id__in=order.clients).values('gender').annotate(count=Count('gender'))
    for i in clients:
        data.append({i['gender']: i['count']})
    return data


def get_clients_data_age(order):
    inter = {}
    clients = Client.objects.all().filter(id__in=order.clients).values('birthdate').annotate(count=Count('birthdate'))
    for i in clients:
        today = datetime.date.today()
        age = today.year - i['birthdate'].year - ((today.month, today.day) < (i['birthdate'].month, i['birthdate'].day))
        if age in inter:
            inter[age] += 1
        else:
            inter[age] = 1
    data = []
    for i in inter.keys():
        data.append({int(i): inter[i]})
    return data
