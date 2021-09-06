# Generated by Django 3.1.4 on 2021-09-06 17:11

from django.db import migrations, models
import orders.models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_id',
            field=models.CharField(blank=True, default=orders.models.random_code, max_length=10, null=True),
        ),
    ]
