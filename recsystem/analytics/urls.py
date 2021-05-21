from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('order/<int:order_id>/', views.order_page, name='order'),
    path('order/new/', views.order_new, name='order_new'),
    path('categories/', views.categories, name='categories'),
    path('orders/confirmed/', views.confirmed_orders, name='confirmed_orders'),
    path('orders/unconfirmed/', views.unconfirmed_orders, name='unconfirmed_orders'),
    path('orders/accepted/', views.accepted_orders, name='accepted_orders'),
    path('orders/completed/', views.completed_orders, name='completed_orders'),
    path('orders/all/', views.all_orders, name='all_orders'),
    path('order/download/', views.order_download, name='order_download'),
    path('order/<int:order_id>/confirm/', views.order_confirm, name='order_confirm'),
    path('order/<int:order_id>/accept/', views.order_accept, name='order_accept'),
    path('order/<int:order_id>/complete/', views.order_complete, name='order_complete'),
    path('order/<int:order_id>/cancel/', views.order_cancel, name='order_cancel'),
    path('contacts/', views.contacts, name='contacts'),
    path('messages/', views.messages_page, name='messages'),
    path('messages/<int:message_id>/read/', views.messages_read, name='messages_read'),
    path('messages/read/all/', views.messages_read_all, name='messages_read_all'),
    path('', views.index, name='index'),
]