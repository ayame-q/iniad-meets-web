# Generated by Django 3.1.7 on 2021-04-20 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meets', '0014_auto_20210420_0916'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='family_name_ruby',
            field=models.CharField(blank=True, default='', max_length=40, null=True, verbose_name='姓(フリガナ)'),
        ),
        migrations.AddField(
            model_name='user',
            name='given_name_ruby',
            field=models.CharField(blank=True, default='', max_length=40, null=True, verbose_name='名(フリガナ)'),
        ),
    ]
