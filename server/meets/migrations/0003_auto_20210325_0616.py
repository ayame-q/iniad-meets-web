# Generated by Django 3.1.7 on 2021-03-24 21:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('meets', '0002_auto_20210325_0433'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='circle',
            name='is_movie_uploaded',
        ),
        migrations.AddField(
            model_name='circle',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.localtime, verbose_name='登録日'),
        ),
        migrations.AddField(
            model_name='circle',
            name='movie_uploaded_at',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='動画アップロード時刻'),
        ),
    ]
