# Generated by Django 2.2.4 on 2019-10-30 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_panel', '0035_auto_20191030_0929'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='service_list',
            options={'verbose_name': 'لیست خدمات', 'verbose_name_plural': 'لیست خدمات'},
        ),
        migrations.AddField(
            model_name='service_list',
            name='code',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]