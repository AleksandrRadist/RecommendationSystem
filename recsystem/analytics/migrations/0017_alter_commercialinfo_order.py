# Generated by Django 3.2.3 on 2021-05-27 20:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0016_auto_20210527_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commercialinfo',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commercial_info', to='analytics.order'),
        ),
    ]
