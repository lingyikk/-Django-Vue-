# Generated by Django 4.2.5 on 2024-04-07 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelorder',
            name='status',
            field=models.CharField(default=None, max_length=10, verbose_name='状态'),
        ),
        migrations.AddField(
            model_name='productorder',
            name='status',
            field=models.CharField(default=None, max_length=10, verbose_name='状态'),
        ),
        migrations.AddField(
            model_name='scenicspotorder',
            name='status',
            field=models.CharField(default=None, max_length=10, verbose_name='状态'),
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]
