# Generated by Django 3.1.7 on 2021-04-20 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meets', '0013_circle_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
        migrations.AddField(
            model_name='circle',
            name='entry_webhook_password',
            field=models.CharField(blank=True, max_length=36, null=True, verbose_name='登録時WebhookPassword'),
        ),
        migrations.AddField(
            model_name='user',
            name='family_name',
            field=models.CharField(blank=True, default='', max_length=40, null=True, verbose_name='姓'),
        ),
        migrations.AddField(
            model_name='user',
            name='given_name',
            field=models.CharField(blank=True, default='', max_length=40, null=True, verbose_name='名'),
        ),
    ]
