# Generated by Django 2.2.4 on 2019-12-19 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('site_panel', '0045_auto_20191219_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deceased',
            name='presenter_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='site_panel.Presenter', verbose_name='معرف '),
        ),
    ]