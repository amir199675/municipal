# Generated by Django 2.2.4 on 2019-10-08 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_panel', '0023_auto_20191008_1216'),
    ]

    operations = [
        migrations.CreateModel(
            name='Send_Letter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=32, verbose_name='کد ')),
                ('description', models.TextField(verbose_name='توضیحات ')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='', verbose_name='تصویر ')),
                ('status', models.CharField(default='Send', max_length=32, verbose_name='وضعیت ')),
            ],
            options={
                'verbose_name': 'بایگانی',
                'verbose_name_plural': 'بایگانی',
                'unique_together': {('code', 'status')},
            },
        ),
    ]
