# Generated by Django 2.2.4 on 2020-01-07 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0043_auto_20200102_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='new',
            name='status',
            field=models.CharField(choices=[('Draft', 'draft'), ('Publish', 'publish')], default='Draft', max_length=32, verbose_name='وضعیت '),
        ),
    ]
