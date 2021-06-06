# Generated by Django 3.2.3 on 2021-06-02 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commercialinfo',
            name='clicked_clients',
            field=models.ManyToManyField(blank=True, related_name='commercial_clicked_clients', to='analytics.Client'),
        ),
        migrations.AlterField(
            model_name='commercialinfo',
            name='performed_action_clients',
            field=models.ManyToManyField(blank=True, related_name='commercial_performed_action_clients', to='analytics.Client'),
        ),
        migrations.AlterField(
            model_name='commercialinfo',
            name='shown_clients',
            field=models.ManyToManyField(blank=True, related_name='commercial_shown_clients', to='analytics.Client'),
        ),
        migrations.AlterField(
            model_name='order',
            name='clients',
            field=models.ManyToManyField(blank=True, to='analytics.Client'),
        ),
        migrations.AlterField(
            model_name='recommendationmodel',
            name='data',
            field=models.ManyToManyField(blank=True, to='analytics.RecommendationData'),
        ),
    ]