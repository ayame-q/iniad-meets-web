# Generated by Django 3.1.7 on 2021-04-12 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meets', '0005_auto_20210326_0950'),
    ]

    operations = [
        migrations.AddField(
            model_name='circle',
            name='thumbnail_uploaded_at',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='サムネイルアップロード時刻'),
        ),
        migrations.AddField(
            model_name='circle',
            name='thumbnail_url',
            field=models.URLField(blank=True, null=True, verbose_name='サムネイルURL'),
        ),
        migrations.AlterField(
            model_name='circle',
            name='comment',
            field=models.TextField(blank=True, default='', max_length=80, verbose_name='一言説明'),
        ),
    ]
