from django.urls import path

from . import views

urlpatterns = [
    path('order/<int:order_id>/', views.order_page, name='order'),
    path('new_order/', views.new_order, name='new_order'),
    path('qwe/', views.load),
    path('', views.index, name='index'),
]