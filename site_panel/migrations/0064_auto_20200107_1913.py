# Generated by Django 2.2.4 on 2020-01-07 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_panel', '0063_auto_20200107_1745'),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(blank=True, max_length=32, null=True, verbose_name='کد ماشین ')),
            ],
            options={
                'verbose_name': 'ماشین ها',
                'verbose_name_plural': 'ماشین ها',
            },
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(blank=True, max_length=8, null=True, unique=True)),
                ('name', models.CharField(max_length=64, verbose_name='مقصد ')),
                ('price', models.CharField(max_length=8, verbose_name='هزینه ')),
            ],
        ),
        migrations.DeleteModel(
            name='Movement_Certificate',
        ),
    ]