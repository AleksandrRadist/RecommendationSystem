# Generated by Django 3.2.3 on 2021-05-25 18:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0013_alter_message_creation_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='transactions_number',
        ),
    ]