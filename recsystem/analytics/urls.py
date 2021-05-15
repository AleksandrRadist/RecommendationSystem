from django.urls import path

from . import views

urlpatterns = [
    path('order/<int:order_id>/', views.order_page, name='order'),
    path('new_order/', views.new_order, name='new_order'),
    path('categories/', views.categories, name='categories'),
    path('order/download/', views.order_download, name='order_download'),
    path('', views.index, name='index'),
]