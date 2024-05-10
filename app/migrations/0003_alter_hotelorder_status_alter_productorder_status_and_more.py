# Generated by Django 4.2.5 on 2024-04-07 18:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_hotelorder_status_productorder_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelorder',
            name='status',
            field=models.CharField(default='已取消', max_length=100, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='productorder',
            name='status',
            field=models.CharField(default='已取消', max_length=100, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='scenicspotorder',
            name='status',
            field=models.CharField(default='已取消', max_length=100, verbose_name='状态'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='评论内容')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='评论时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user')),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论',
            },
        ),
    ]
