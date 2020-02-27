# Generated by Django 2.2.4 on 2020-02-19 21:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('site_panel', '0080_auto_20200118_1136'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grave_Stone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('buyer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='site_panel.Buyer')),
                ('deceased_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='site_panel.Deceased')),
            ],
        ),
    ]