# Generated by Django 2.2.4 on 2019-09-23 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_panel', '0014_auto_20190923_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='ghete',
            field=models.CharField(blank=True, default='', max_length=4, null=True, verbose_name='قطعه '),
        ),
    ]
