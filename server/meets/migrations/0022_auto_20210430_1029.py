# Generated by Django 3.1.7 on 2021-04-30 01:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('meets', '0021_auto_20210429_1544'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entry',
            options={'ordering': ['created_at']},
        ),
        migrations.AddField(
            model_name='user',
            name='last_connected_at',
            field=models.DateTimeField(default=django.utils.timezone.localtime, verbose_name='最終接続時刻'),
        ),
    ]
