# Generated by Django 4.2.5 on 2023-09-12 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom_api', '0005_rename_sellerproduct_product_seller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='username',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
