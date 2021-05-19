import csv
import datetime
import uuid
from django.shortcuts import get_object_or_404
import pytz
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import OrderForm
from .models import Client, Category, Transaction, Subscription, Order


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


def order_new(request):
    if request.method == 'POST':
        form = OrderForm(request.POST or None)

        if form.is_valid():
            order = form.save(commit=False)
            category = Category.objects.get(name=order.category)
            transactions = Transaction.objects.filter(product_category=category.id)
            order.transactions_number = transactions.count()
            clients = []
            for i in transactions.values('client_id').distinct():
                clients.append(i['client_id'])
            order.clients = clients
            order.clients_number = len(order.clients)
            delta = order.date_end - order.date_start
            order.days = delta.days + 1
            price = (order.days // 7 + 1) * 20 * order.clients_number
            order.price = price
            order.code = uuid.uuid4().hex[:10].upper()
            order.save()
            return redirect('order', order_id=order.pk)

        return render(request, 'new_order.html', {'form': form})

    form = OrderForm()
    return render(request, 'new_order.html', {'form': form})


def order_page(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order.html',
                  {'order': order})


def order_confirm(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.confirmation_status = True
    order.save()
    return redirect('order', order_id=order_id)


def order_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.acceptance_status:
        return redirect('order', order_id=order_id)
    order.confirmation_status = False
    order.save()
    return redirect('order', order_id=order_id)


def index(request):
    if request.method == 'POST':
        order_code = request.POST.get('search', '')
        try:
            order = Order.objects.get(code=order_code)
            return redirect('order', order.id)
        except Order.DoesNotExist:
            return render(request, 'index.html', {'flag': 1})
    return render(request, 'index.html')


def categories(request):
    items = Category.objects.all()
    return render(request, 'category_list.html',
                  {'items': items})


def order_download(request):
    ingredient_txt = ['u are trash']
    file = 'stats.txt'
    response = HttpResponse(ingredient_txt, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={file}'
    return response
