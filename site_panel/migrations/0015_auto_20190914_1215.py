# Generated by Django 2.2.4 on 2019-09-14 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_panel', '0014_auto_20190913_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='death_certificate',
            name='date_of_death',
            field=models.DateField(blank=True, null=True, verbose_name='تاریخ فوت '),
        ),
    ]
