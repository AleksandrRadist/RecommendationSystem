from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
import csv
import datetime
import pytz
from .models import Client, Category, Transaction, Subscription, Order
from .forms import OrderForm


def load(request):
    with open("analytics/subscriptions.csv", encoding='utf-8') as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        data_read = [row for row in reader]
        for row in data_read[1::]:
            q = None
            if row[6] != '':
                q = datetime.datetime.strptime(row[6], "%Y-%m-%d").date()
            _, created = Subscription.objects.get_or_create(
                id=row[0],
                client_id=int(row[1]),
                product_category=int(row[2]),
                product_company=row[3],
                amount=float(row[4]),
                date_start=datetime.datetime.strptime(row[5], "%Y-%m-%d").date(),
                date_end=q
            )
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
    with open("analytics/transactions.csv", encoding='utf-8') as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        data_read = [row for row in reader]
        for row in data_read[1::]:
            q = datetime.datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S')
            q = pytz.utc.localize(q)
            _, created = Transaction.objects.get_or_create(
                id=row[0],
                client_id=int(row[1]),
                product_category=int(row[2]),
                product_company=row[3],
                subtype=row[4],
                amount=float(row[5]),
                date=q,
                transaction_type=row[7]
            )
    return render(request, 'index.html')


def new_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST or None)

        if form.is_valid():
            order_new = form.save(commit=False)
            category_id = Category.objects.filter(name=order_new.category)
            transactions = Transaction.objects.filter(product_category__in=category_id)
            order_new.transactions_number = transactions.count()
            order_new.clients_number = transactions.values('client_id').distinct().count()
            delta = order_new.date_end - order_new.date_start
            order_new.days = delta.days + 1
            price = order_new.days // 7 + 1 * 20 * order_new.clients_number
            order_new.price = price
            order_new.save()
            return redirect('order', order_id=order_new.pk)

        return render(request, 'new_order.html', {'form': form})

    form = OrderForm()
    return render(request, 'new_order.html', {'form': form})


def order_page(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'order.html',
                  {'order': order})


def index(request):
    return render(request, 'index.html')
