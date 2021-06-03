import datetime
import uuid

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.urls import reverse
from recsystem.settings import paginator_items_on_page

from .forms import OrderForm, MessageForm
from .models import Category, Order, Message, CommercialInfo
from .utils import get_clients_data_gender, get_clients_data_age, \
    commercial_fake_info, get_recommendation_model_data, commercial_fake_forecast_info


def order_new(request):
    if request.method == 'POST':
        form = OrderForm(request.POST or None)
        if form.is_valid():
            order = form.save(commit=False)
            category = Category.objects.get(name=order.category)
            delta = order.date_end - order.date_start
            order.days = delta.days + 1
            order.code = uuid.uuid4().hex[:10].upper()
            order.save()
            data = get_recommendation_model_data('version1')
            clients = []
            if data.filter(category=category).exists():
                clients = data.get(category=category).clients
            for i in clients.all():
                order.clients.add(i)
            order.clients_number = order.clients.count()
            order.price = (order.days // 7 + 1) * 20 * order.clients_number
            forecast_data = commercial_fake_forecast_info(order)
            order.forecast_conversion_rate = forecast_data['conversion_rate']
            order.forecast_click_through_rate = forecast_data['click_through_rate']
            order.forecast_cost_per_action = forecast_data['cpa']
            order.forecast_cost_per_click = forecast_data['cpc']
            order.save()
            return redirect('order', order_id=order.pk)
        return render(request, 'new_order.html', {'form': form})
    form = OrderForm()
    return render(request, 'new_order.html', {'form': form})


def order_page(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order.html',
                  {'order': order})


def order_commercial_info(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    info = get_object_or_404(CommercialInfo, order=order)
    conversion_rate, click_through_rate = 0, 0
    cpc = 'Пока ни один клиент не перешел по ссылке'
    cpa = 'Пока ни один клиент не выполнил целевое действие'
    if info.clicked_number != 0:
        conversion_rate = round(info.performed_action_number / info.clicked_number * 100, 2)
        cpc = round(order.price / info.clicked_number, 2)
    if info.shown_number != 0:
        click_through_rate = round(info.clicked_number / info.shown_number * 100, 2)
    if info.performed_action_number != 0:
        cpa = round(order.price / info.performed_action_number, 2)
    flag = request.GET.get('clients', 'shown')
    return render(request, 'commercial_info.html',
                  {'info': info,
                   'conversion_rate': conversion_rate,
                   'click_through_rate': click_through_rate,
                   'cpa': cpa,
                   'cost_per_click': cpc,
                   'clients': flag})


def order_confirm(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.confirmation_status = True
    order.save()
    return redirect('order', order_id=order_id)


@login_required
def order_accept(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if not order.confirmation_status:
        return render(request, 'order.html', {
            'order': order,
            'message': 'Нельзя принять неподтвержденный заказ!'
        })
    if order.acceptance_status:
        return render(request, 'order.html', {
            'order': order,
            'message': 'Заказ уже был принят!'
        })
    if order.completion_status:
        return render(request, 'order.html', {
            'order': order,
            'message': 'Заказ уже был выполнен!'
        })
    order.acceptance_status = True
    order.acceptance_date = datetime.datetime.now()
    order.save()
    return redirect('order', order_id=order_id)


@login_required
def order_complete(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if not order.confirmation_status:
        return render(request, 'order.html', {
            'order': order,
            'message': 'Нельзя выполнить неподтвержденный заказ!'
        })
    if not order.acceptance_status:
        return render(request, 'order.html', {
            'order': order,
            'message': 'Нельзя выполнить непринятый заказ!'
        })
    if order.completion_status:
        return render(request, 'order.html', {
            'order': order,
            'message': 'Заказ уже был выполнен!'
        })
    order.completion_status = True
    order.completion_date = datetime.datetime.now()
    order.save()
    info = CommercialInfo(order=order)
    info.save()
    commercial_fake_info(info.id)
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
    demo = request.GET.get('demo', None)
    if demo is None:
        return render(request, 'index.html')
    return render(request, 'index.html', {'demo': True})


def demo_notification(request):
    return redirect('/?demo=True')


def categories(request):
    items = Category.objects.all()
    paginator = Paginator(items, paginator_items_on_page)
    page_number = request.GET.get(
        'page')
    page = paginator.get_page(
        page_number)
    return render(request, 'category_list.html',
                  {'page': page})


def order_download(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    data = [
        ('Код заказа', order.code),
        ('Компания', order.company_name),
        ('Email', order.email),
        ('Количество клиентов', order.clients_number),
        ('Дата начала', order.date_start),
        ('Дата окончания', order.date_end),
        ('Всего дней', order.days),
        ('Ожидаемая цена услуги', order.price)
    ]
    gender_data = get_clients_data_gender(order.clients)
    age_data = get_clients_data_age(order.clients)
    data_txt = [
        (f"\u2022 {item[0].capitalize()}"
         f"\ufe55 {item[1]} \n")
        for item in data
    ]
    data_txt.append(f"\u2022 {'Соотношение полов клиентов'}\ufe55 \n")
    for i in gender_data:
        data_txt.append(f"\u2012 {i} \n")
    data_txt.append(f"\u2022 {'Возраст клиентов'}\ufe55 \n")
    for i in age_data:
        data_txt.append(f"\u2012 {i} \n")
    file = 'order_data.txt'
    response = HttpResponse(data_txt, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={file}'
    return response


@login_required
def orders_page(request):
    order_filter = request.GET.get('filter', 'All')
    if order_filter == 'unconfirmed':
        orders = Order.objects.order_by('-creation_date').filter(confirmation_status=False)
        order_filter = 'Неподтвержденные'
    elif order_filter == 'confirmed':
        orders = Order.objects.filter(confirmation_status=True, acceptance_status=False).order_by('-creation_date')
        order_filter = 'Подтвержденные'
    elif order_filter == 'accepted':
        orders = Order.objects.filter(acceptance_status=True, completion_status=False).order_by('-acceptance_date')
        order_filter = 'Принятые'
    elif order_filter == 'completed':
        orders = Order.objects.filter(completion_status=True).order_by('-completion_date')
        order_filter = 'Выполненные'
    else:
        orders = Order.objects.order_by('-creation_date').all()
        order_filter = 'Все'
    paginator = Paginator(orders, paginator_items_on_page)
    page_number = request.GET.get(
        'page')
    page = paginator.get_page(
        page_number)
    return render(request, 'orders.html',
                  {'page': page,
                   'filter': order_filter})


def contacts(request):
    if request.method == 'POST':
        form = MessageForm(request.POST or None)

        if form.is_valid():
            form.save()
            form = MessageForm()
            return render(request, 'contacts.html', {'form': form, 'flag': True})

        return render(request, 'contacts.html', {'form': form})

    form = MessageForm()
    return render(request, 'contacts.html', {'form': form})


@login_required
def all_messages(request):
    messages = Message.objects.order_by('-creation_date')
    paginator = Paginator(messages, paginator_items_on_page)
    page_number = request.GET.get(
        'page')
    page = paginator.get_page(
        page_number)
    return render(request, 'messages.html',
                  {'page': page})


@login_required
def new_messages(request):
    messages = Message.objects.filter(read_status=False).order_by('-creation_date')
    paginator = Paginator(messages, paginator_items_on_page)
    page_number = request.GET.get(
        'page')
    page = paginator.get_page(
        page_number)
    return render(request, 'new_messages.html',
                  {'page': page})


@login_required
def read_messages(request):
    messages = Message.objects.filter(read_status=True).order_by('-creation_date')
    paginator = Paginator(messages, paginator_items_on_page)
    page_number = request.GET.get(
        'page')
    page = paginator.get_page(
        page_number)
    return render(request, 'read_messages.html',
                  {'page': page})


@login_required
def messages_page(request):
    message_filter = request.GET.get('filter', 'All')
    if message_filter == 'new':
        messages = Message.objects.filter(read_status=False).order_by('-creation_date')
        message_filter = 'Новые'
    elif message_filter == 'read':
        messages = Message.objects.filter(read_status=True).order_by('-creation_date')
        message_filter = 'Прочитанные'
    else:
        messages = Message.objects.order_by('-creation_date')
        message_filter = 'Все'
    paginator = Paginator(messages, paginator_items_on_page)
    page_number = request.GET.get(
        'page')
    page = paginator.get_page(
        page_number)
    return render(request, 'messages.html',
                  {'page': page,
                   'filter': message_filter})


@login_required
def messages_read(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    message.read_status = True
    message.save()
    url = reverse('messages')
    if request.GET.get('previous', None) is not None:
        url += '?filter=new'
    return redirect(url)


@login_required
def messages_read_all(request):
    messages = Message.objects.all()
    messages.update(read_status=True)
    url = reverse('messages')
    if request.GET.get('previous', None) is not None:
        url += '?filter=new'
    return redirect(url)
