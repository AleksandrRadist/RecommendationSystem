from django.db import models
import datetime

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
    mcc_code = models.CharField(max_length=300)


class Transaction(models.Model):
    id = models.IntegerField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product_company = models.CharField(max_length=100)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subtype = models.CharField(max_length=20)
    amount = models.FloatField()
    date = models.DateTimeField()
    transaction_type = models.CharField(max_length=20)


class Subscription(models.Model):
    id = models.IntegerField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_company = models.CharField(max_length=100)
    date_start = models.DateField()
    date_end = models.DateField(null=True)
    amount = models.FloatField()


class Order(models.Model):
    code = models.CharField(unique=True, max_length=10)
    email = models.EmailField()
    company_name = models.CharField(max_length=100, default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    clients_number = models.IntegerField(default=0)
    clients = models.ManyToManyField(Client, blank=True)
    date_start = models.DateField(default=datetime.date.today)
    date_end = models.DateField(default=datetime.date.today)
    days = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    confirmation_status = models.BooleanField(default=False)
    completion_status = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True, null=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    acceptance_status = models.BooleanField(default=False)
    acceptance_date = models.DateTimeField(null=True, blank=True)
    forecast_conversion_rate = models.FloatField(default=0)
    forecast_click_through_rate = models.FloatField(default=0)
    forecast_cost_per_action = models.FloatField(default=0)
    forecast_cost_per_click = models.FloatField(default=0)


class Message(models.Model):
    text = models.TextField()
    email = models.EmailField()
    read_status = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)


class CommercialInfo(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE,
                                 related_name='commercial_info')
    shown_number = models.IntegerField(default=0)
    clicked_number = models.IntegerField(default=0)
    shown_clients = models.ManyToManyField(Client, related_name='commercial_shown_clients',
                                           blank=True)
    clicked_clients = models.ManyToManyField(Client, related_name='commercial_clicked_clients',
                                             blank=True)
    performed_action_clients = models.ManyToManyField(Client, related_name='commercial_performed_action_clients',
                                                      blank=True)
    performed_action_number = models.IntegerField(default=0)


class RecommendationData(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client, blank=True)


class RecommendationModel(models.Model):
    name = models.CharField(max_length=200)
    data = models.ManyToManyField(RecommendationData, blank=True)
    last_update = models.DateTimeField(blank=True, null=True)
    f_score = models.FloatField(default=0)

