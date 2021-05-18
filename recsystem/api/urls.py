from django.urls import path

from .views import (api_orders, api_orders_client, api_orders_detail)

urlpatterns = [
    path('orders/', api_orders, name='api_orders'),
    path('orders/<int:order_id>/', api_orders_detail, name='api_orders_detail'),
    path('orders/<string:code>/client/', api_orders_client, name='api_orders_client'),
]