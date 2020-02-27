# Generated by Django 2.2.4 on 2020-01-18 09:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('seen', '0005_auto_20200115_1351'),
    ]

    operations = [
        migrations.CreateModel(
            name='Last_Seen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('date', models.DateField()),
                ('name', models.CharField(max_length=64)),
                ('path', models.CharField(max_length=504)),
                ('counter', models.CharField(default=0, max_length=64)),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]