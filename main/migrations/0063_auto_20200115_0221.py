# Generated by Django 2.2.4 on 2020-01-15 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0062_auto_20200115_0220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='new',
            name='status',
            field=models.CharField(choices=[('Publish', 'publish'), ('Draft', 'draft')], default='Draft', max_length=32, verbose_name='وضعیت '),
        ),
    ]
