# Generated by Django 2.2.4 on 2019-12-29 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_auto_20191229_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='new',
            name='status',
            field=models.CharField(choices=[('Publish', 'publish'), ('Draft', 'draft')], default='Draft', max_length=32, verbose_name='وضعیت '),
        ),
    ]
