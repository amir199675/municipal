# Generated by Django 2.2.4 on 2019-12-31 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_panel', '0053_auto_20191229_1817'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='factor_id',
        ),
        migrations.AddField(
            model_name='bill',
            name='document',
            field=models.CharField(default=1, max_length=32),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Factor',
        ),
    ]
