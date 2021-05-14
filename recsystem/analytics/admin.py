from django.contrib import admin

from .models import Client, Category, Transaction, Subscription, Order


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'email', 'phone_number',)
    search_fields = ('fullname',)
    list_filter = ('fullname',)
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_id', 'product_category', 'product_company', 'amount', 'date',)
    search_fields = ('id',)
    list_filter = ('date',)
    empty_value_display = '-пусто-'


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_id', 'product_category', 'product_company', 'amount', 'date_start', 'date_end',)
    search_fields = ('id',)
    list_filter = ('date_start',)
    empty_value_display = '-пусто-'


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'category',)
    empty_value_display = '-пусто-'


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
