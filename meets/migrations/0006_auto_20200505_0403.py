# Generated by Django 3.0.5 on 2020-05-04 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meets', '0005_chatlog_sender_circle'),
    ]

    operations = [
        migrations.AddField(
            model_name='circle',
            name='comment',
            field=models.TextField(blank=True, default='', verbose_name='一言説明'),
        ),
        migrations.AddField(
            model_name='circle',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='開始予定日時'),
        ),
        migrations.AddField(
            model_name='circle',
            name='twitter_sn',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Twitter ID'),
        ),
    ]