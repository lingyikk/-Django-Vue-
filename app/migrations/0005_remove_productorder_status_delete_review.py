# Generated by Django 4.2.5 on 2024-04-07 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_hotelorder_status_alter_product_sales_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productorder',
            name='status',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]
