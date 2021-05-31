from .models import Client, CommercialInfo, RecommendationModel, RecommendationData, Category
from django.db.models import Count
import datetime
from django.shortcuts import get_object_or_404
import random
import sys
sys.path.insert(1, '/home/bi2021/RecommendationSystem/model/final_model/')
from model import model as updated_model_data


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


def get_recommendation_model_data(name):
    model = RecommendationModel.objects.get(name=name)
    if model.last_update is None or model.last_update.date() != datetime.datetime.now().date():
        model_data, f = updated_model_data()
        # model_data, f = {1: [1, 2, 3]}, 4
        for i in model_data.keys():
            category = Category.objects.get(id=i)
            if model.data.filter(category=category).exists():
                data = RecommendationData.objects.get(category=category)
                data.clients = model_data[i]
                data.save()
            else:
                data = RecommendationData.objects.create(category=category, clients=model_data[i])
                model.data.add(data)
        model.last_update = datetime.datetime.now()
        model.f_score = f
        model.save()
    return model.data.all()


def commercial_fake_forecast_info(order):
    conversion_rate = round(random.random(), 2)
    click_through_rate = round(random.random(), 2)
    cpa = round(order.price / click_through_rate / order.clients_number / conversion_rate, 2)
    cpc = round(order.price / click_through_rate / order.clients_number, 2)
    return {'conversion_rate': conversion_rate * 100,
            'click_through_rate': click_through_rate * 100,
            'cpc': cpc,
            'cpa': cpa}
