from django import forms
from .models import Order
from tempus_dominus.widgets import DatePicker

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('company_name', 'category', 'date_start', 'date_end',)
        help_texts = {
            'date_start': 'Please enter date in "YYYY-mm-dd" format',
            'date_end': 'You can double-click to activate datepicker',
        }
        widgets = {
            'date_start': DatePicker(),
            'date_end': DatePicker()
        }
