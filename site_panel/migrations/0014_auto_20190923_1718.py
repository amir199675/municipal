# Generated by Django 2.2.4 on 2019-09-23 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('site_panel', '0013_auto_20190921_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place_service',
            name='place_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='place_service', to='site_panel.Place', verbose_name='قبر '),
        ),
    ]