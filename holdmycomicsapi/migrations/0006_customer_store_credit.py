# Generated by Django 4.1.3 on 2023-10-01 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('holdmycomicsapi', '0005_customer_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='store_credit',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
