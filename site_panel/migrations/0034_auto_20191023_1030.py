# Generated by Django 2.2.4 on 2019-10-23 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_panel', '0033_auto_20191022_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cause_death',
            name='name',
            field=models.CharField(max_length=128, unique=True, verbose_name='عنوان '),
        ),
    ]
