from django import forms
from .models import Order, Message
from tempus_dominus.widgets import DatePicker
import datetime


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('company_name', 'email', 'category', 'date_start', 'date_end',)
        help_texts = {
            'date_start': 'Please enter date in "YYYY-mm-dd" format',
            'date_end': 'You can double-click to activate datepicker',
        }
        widgets = {
            'date_start': DatePicker(),
            'date_end': DatePicker()
        }

    def clean(self):
        form_data = self.cleaned_data
        deadline = (datetime.datetime.today() + datetime.timedelta(days=10)).date()
        date_start = form_data['date_start']
        date_end = form_data['date_end']
        if date_start > date_end:
            self._errors["Конечная дата не может быть раньше начальной даты"] = [
                "Конечная дата не может быть раньше начальной даты"
            ]
        if date_start < deadline:
            self._errors["Работа рекламы не может начаться ранее чем через 10 дней после создания заказа"] = [
                "Работа рекламы не может начаться ранее чем через 10 дней после создания заказа"
            ]
        if date_end < deadline:
            self._errors["Работа рекламы не может начаться ранее чем через 10 дней после создания заказа"] = [
                "Работа рекламы не может начаться ранее чем через 10 дней после создания заказа"
            ]
        return form_data


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('text', 'email',)