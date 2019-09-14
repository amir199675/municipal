# Generated by Django 2.2.4 on 2019-09-08 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_panel', '0010_auto_20190907_1308'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deceased',
            name='name',
        ),
        migrations.AddField(
            model_name='deceased',
            name='first_name',
            field=models.CharField(default='first name', max_length=64, verbose_name='نام '),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deceased',
            name='last_name',
            field=models.CharField(default='first name', max_length=64, verbose_name='نام خانوادگی '),
            preserve_default=False,
        ),
    ]
