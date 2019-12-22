# Generated by Django 2.2.4 on 2019-12-19 11:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('site_panel', '0044_auto_20191218_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر '),
        ),
        migrations.AlterField(
            model_name='presenter',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر '),
        ),
    ]
