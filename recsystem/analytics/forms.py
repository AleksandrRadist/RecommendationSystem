from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('company_name', 'category', 'date_start', 'date_end',)
        help_texts = {
            'date_start': 'Please enter date in "YYYY-mm-dd" format',
            'date_end': 'Please enter date in "YYYY-mm-dd" format',
        }
