# Generated by Django 2.2.4 on 2020-01-02 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0040_auto_20200102_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='new',
            name='status',
            field=models.CharField(choices=[('Publish', 'publish'), ('Draft', 'draft')], default='Draft', max_length=32, verbose_name='وضعیت '),
        ),
    ]
