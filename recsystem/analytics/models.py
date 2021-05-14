from django.db import models
import datetime

class Client(models.Model):
    id = models.IntegerField(primary_key=True)
    fullname = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=50)
    email = models.EmailField()
    workplace = models.CharField(max_length=200)
    birthdate = models.DateField()
    registration_date = models.DateField()
    gender = models.CharField(max_length=1)
    income = models.FloatField()
    expenses = models.FloatField()
    deposit = models.BooleanField()
    credit = models.BooleanField()


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    mcc_code = models.CharField(max_length=100)


class Transaction(models.Model):
    id = models.IntegerField(primary_key=True)
    client_id = models.IntegerField()
    product_company = models.CharField(max_length=100)
    product_category = models.IntegerField()
    subtype = models.CharField(max_length=20)
    amount = models.FloatField()
    date = models.DateTimeField()
    transaction_type = models.CharField(max_length=20)


class Subscription(models.Model):
    id = models.IntegerField(primary_key=True)
    client_id = models.IntegerField()
    product_category = models.IntegerField()
    product_company = models.CharField(max_length=100)
    date_start = models.DateField()
    date_end = models.DateField(null=True)
    amount = models.FloatField()


class Order(models.Model):
    company_name = models.CharField(max_length=100, default='')
    CATEGORY_CHOICES = [
        ('Каршеринг', 'Каршеринг'),
        ('Супермаркеты', 'Супермаркеты'),
        ('Такси', 'Такси'),
        ('Музыка', 'Музыка'),
        ('Фастфуд', 'Фастфуд'),
        ('Транспорт', 'Транспорт'),
        ('Аптеки', 'Аптеки'),
        ('Кино', 'Кино'),
        ('Книги', 'Книги'),
        ('Развелечения', 'Развлечения'),
        ('Красота', 'Красота'),
        ('Образование', 'Образование'),
        ('Одежда и обувь', 'Одежда и обувь'),
        ('Рестораны', 'Рестораны'),
        ('Топливо', 'Топливо'),
        ('Животные', 'Животные'),
        ('Дом и ремонт', 'Дом и ремонт'),
        ('Спорттовары', 'Спорттовары'),
        ('Сувениры', 'Сувениры'),
        ('Фото и видео', 'Фото и видео'),
        ('Цветы', 'Цветы'),
        ('Аренда авто', 'Аренда авто'),
        ('Автоуслуги', 'Автоуслуги'),
        ('Авиабилеты', 'Авиабилеты'),
        ('Дьюти-фри', 'Дьюти-фри'),
        ('Железнодорожные билеты', 'Железнодорожные билеты'),
        ('Искусство', 'Искусство'),
        ('Переводы', 'Переводы'),
        ('Другое', 'Другое')
    ]
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    transactions_number = models.IntegerField(default=0)
    clients_number = models.IntegerField(default=0)
    date_start = models.DateField(default=datetime.date.today)
    date_end = models.DateField(default=datetime.date.today)
    days = models.IntegerField(default=0)
    price = models.FloatField(default=0)
