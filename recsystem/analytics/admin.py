from django.contrib import admin

from .models import Client, Category, Transaction, Subscription, Order, Message, CommercialInfo


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'email', 'phone_number',)
    search_fields = ('fullname',)
    list_filter = ('gender',)
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_id', 'product_category', 'product_company', 'amount', 'date',)
    search_fields = ('product_company',)
    list_filter = ('product_category',)
    empty_value_display = '-пусто-'


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_id', 'product_category', 'product_company', 'amount', 'date_start', 'date_end',)
    search_fields = ('product_company',)
    list_filter = ('product_category',)
    empty_value_display = '-пусто-'


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'company_name')
    readonly_fields = ('creation_date',)
    list_filter = ('category',)
    empty_value_display = '-пусто-'


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'email',)
    readonly_fields = ('creation_date',)
    empty_value_display = '-пусто-'


class CommercialInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'shown_number', 'clicked_number', 'performed_action_number',)
    empty_value_display = '-пусто-'


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(CommercialInfo, CommercialInfoAdmin)
