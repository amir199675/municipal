# Generated by Django 2.2.4 on 2019-09-24 22:47

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('site_panel', '0018_auto_20190924_1833'),
    ]

    operations = [
        migrations.CreateModel(
            name='Additional_Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='نام خدمات ')),
                ('price', models.CharField(max_length=8, verbose_name='هزینه ')),
                ('status', models.CharField(choices=[('PAID', 'پرداخت شده'), ('NOT PAID', 'پرداخت نشده')], default='NOT PAID', max_length=32, verbose_name='وضعیت پرداخت ')),
                ('buyer_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.fields.CharField, to='site_panel.Buyer', verbose_name='خریدار ')),
                ('deceased_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additional_service', to='site_panel.Deceased', verbose_name='متوفی ')),
            ],
            options={
                'verbose_name': 'خدمات اضافه',
                'verbose_name_plural': 'خدمات اضافه',
            },
        ),
        migrations.AddField(
            model_name='bill',
            name='additional_service_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='site_panel.Additional_Service', verbose_name='خدمات اضافه مربوطه '),
        ),
    ]