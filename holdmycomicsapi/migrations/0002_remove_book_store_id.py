# Generated by Django 4.1.3 on 2023-08-17 02:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('holdmycomicsapi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='store_id',
        ),
    ]
