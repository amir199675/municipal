# Generated by Django 2.2.4 on 2019-10-30 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_auto_20191023_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='new',
            name='status',
            field=models.CharField(choices=[('Draft', 'draft'), ('Publish', 'publish')], default='Draft', max_length=32, verbose_name='وضعیت '),
        ),
    ]
