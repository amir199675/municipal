# Generated by Django 2.2.4 on 2020-01-12 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_panel', '0067_auto_20200112_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movement_service',
            name='status',
            field=models.CharField(choices=[('confirmation', 'تایید شده'), ('disapproval', 'در حال بررسی')], default='NOT PAID', max_length=32, verbose_name='وضعیت پرداخت '),
        ),
    ]
