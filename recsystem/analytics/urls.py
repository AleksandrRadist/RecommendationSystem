from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from . import poll_views

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('demo/',  views.demo_notification, name='demo'),
    path('order/<int:order_id>/', views.order_page, name='order'),
    path('order/<int:order_id>/commercial_info/', views.order_commercial_info, name='order_commercial_info'),
    path('order/data/gender/<int:order_id>/', poll_views.order_data_gender, name='order_data_gender'),
    path('order/data/age/<int:order_id>/', poll_views.order_data_age, name='order_data_age'),
    path('order/new/', views.order_new, name='order_new'),
    path('categories/', views.categories, name='categories'),
    path('orders/', views.orders_page, name='orders'),
    path('order/<int:order_id>/?download/', views.order_download, name='order_download'),
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
