# Generated by Django 2.2.4 on 2019-11-30 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_panel', '0037_auto_20191101_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archive',
            name='status',
            field=models.CharField(choices=[('Inbox', 'دریافتی'), ('Send', 'ارسالی')], default='Send', max_length=32, verbose_name='وضعیت '),
        ),
    ]
