from django.urls import path

from .views import (api_orders, api_orders_client, api_orders_detail)

urlpatterns = [
    path('orders/', api_orders, name='orders'),
    path('orders/<int:order_id>/', api_orders_detail, name='orders_detail'),
    path('orders/<int:order_id>/client/', api_orders_client, name='orders_client'),
]