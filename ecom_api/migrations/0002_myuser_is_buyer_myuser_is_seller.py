# Generated by Django 4.2.5 on 2023-09-06 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='is_buyer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='myuser',
            name='is_seller',
            field=models.BooleanField(default=False),
        ),
    ]
