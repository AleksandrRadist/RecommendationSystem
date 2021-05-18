from django.urls import path

from . import views

urlpatterns = [
    path('order/<int:order_id>/', views.order_page, name='order'),
    path('order/new/', views.order_new, name='order_new'),
    path('categories/', views.categories, name='categories'),
    path('order/download/', views.order_download, name='order_download'),
    path('order/confirm/<int:order_id>/', views.order_confirm, name='order_confirm'),
    path('order/cancel/<int:order_id>/', views.order_cancel, name='order_cancel'),
    path('', views.index, name='index'),
]