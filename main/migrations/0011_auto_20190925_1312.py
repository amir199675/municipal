# Generated by Django 2.2.4 on 2019-09-25 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20190924_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='new',
            name='status',
            field=models.CharField(choices=[('Publish', 'publish'), ('Draft', 'draft')], default='Draft', max_length=32, verbose_name='وضعیت '),
        ),
    ]
