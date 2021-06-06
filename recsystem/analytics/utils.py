import csv
import datetime
import random

import pytz
from django.db.models import Count
from django.shortcuts import get_object_or_404

from .models import Client, CommercialInfo, RecommendationModel, Category, Subscription, Transaction


def get_clients_data_gender(clients):
    data = []
    clients = clients.values('gender').annotate(count=Count('gender'))
    for i in clients:
        data.append({i['gender']: i['count']})
    return data


def get_clients_data_age(clients):
    inter = {}
    clients = clients.values('birthdate').annotate(count=Count('birthdate'))
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
    for i in clients.all()[:info.shown_number]:
        info.shown_clients.add(i)
    for i in clients.all()[:info.clicked_number]:
        info.clicked_clients.add(i)
    for i in clients.all()[:info.performed_action_number]:
        info.performed_action_clients.add(i)
    info.save()


def get_recommendation_model_data(name):
    model = RecommendationModel.objects.get(name=name)
    return model.data.all()


def commercial_fake_forecast_info(order):
    cpa, cpc, conversion_rate, click_through_rate = 0, 0, 0, 0
    if order.clients_number != 0:
        conversion_rate = round(random.random(), 2)
        click_through_rate = round(random.random(), 2)
        cpa = round(order.price / click_through_rate / order.clients_number / conversion_rate, 2)
        cpc = round(order.price / click_through_rate / order.clients_number, 2)
    return {'conversion_rate': conversion_rate * 100,
            'click_through_rate': click_through_rate * 100,
            'cpc': cpc,
            'cpa': cpa}


def load():
    with open("analytics/fgh.csv", encoding='utf-8') as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        data_read = [row for row in reader]
        for row in data_read[1::]:
            _, created = Category.objects.get_or_create(
                id=row[0],
                name=row[1],
                description=row[2],
                mcc_code=row[3]
            )
    with open("analytics/clients.csv", encoding='utf-8') as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        data_read = [row for row in reader]
        for row in data_read[1::]:
            q = 0
            if row[9] != '':
                q = float(row[9])
            _, created = Client.objects.get_or_create(
                id=row[0],
                fullname=row[1],
                address=row[2],
                phone_number=row[3],
                email=row[4],
                workplace=row[5],
                birthdate=datetime.datetime.strptime(row[6], "%Y-%m-%d").date(),
                registration_date=datetime.datetime.strptime(row[7], "%Y-%m-%d").date(),
                gender=row[8],
                income=q,
                expenses=float(row[10]),
                credit=bool(row[11]),
                deposit=bool(row[12])
            )
    with open("analytics/subscriptions.csv", encoding='utf-8') as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        data_read = [row for row in reader]
        for row in data_read[1::]:
            q = None
            if row[6] != '':
                q = datetime.datetime.strptime(row[6], "%Y-%m-%d").date()
            category = Category.objects.get(id=int(row[2]))
            client = Client.objects.get(id=int(row[1]))
            _, created = Subscription.objects.get_or_create(
                id=row[0],
                client=client,
                product_category=category,
                product_company=row[3],
                amount=float(row[4]),
                date_start=datetime.datetime.strptime(row[5], "%Y-%m-%d").date(),
                date_end=q
            )
    with open("analytics/transactions.csv", encoding='utf-8') as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        data_read = [row for row in reader]
        for row in data_read[1::]:
            q = datetime.datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S')
            q = pytz.utc.localize(q)
            category = Category.objects.get(id=int(row[2]))
            client = Client.objects.get(id=int(row[1]))
            _, created = Transaction.objects.get_or_create(
                id=row[0],
                client=client,
                product_category=category,
                product_company=row[3],
                subtype=row[4],
                amount=float(row[5]),
                date=q,
                transaction_type=row[7]
            )