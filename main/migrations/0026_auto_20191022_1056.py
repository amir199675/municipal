# Generated by Django 2.2.4 on 2019-10-22 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_auto_20191022_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='new',
            name='status',
            field=models.CharField(choices=[('Publish', 'publish'), ('Draft', 'draft')], default='Draft', max_length=32, verbose_name='وضعیت '),
        ),
    ]
