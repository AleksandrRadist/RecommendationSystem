from .models import Client, CommercialInfo
from django.db.models import Count
import datetime
from django.shortcuts import get_object_or_404
import random


def get_clients_data_gender(clients):
    data = []
    clients = Client.objects.filter(id__in=clients).values('gender').annotate(count=Count('gender'))
    for i in clients:
        data.append({i['gender']: i['count']})
    return data


def get_clients_data_age(clients):
    inter = {}
    clients = Client.objects.all().filter(id__in=clients).values('birthdate').annotate(count=Count('birthdate'))
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


def commercial_fake_info(info_id):
    info = get_object_or_404(CommercialInfo, id=info_id)
    clients_number = info.order.clients_number
    clients = info.order.clients
    info.shown_number = random.randint(0, clients_number)
    info.clicked_number = random.randint(0, info.shown_number)
    info.performed_action_number = random.randint(0, info.clicked_number)
    info.shown_clients = clients[0:info.shown_number:]
    info.clicked_clients = clients[0:info.clicked_number:]
    info.performed_action_clients = clients[0:info.performed_action_number:]
    info.save()
