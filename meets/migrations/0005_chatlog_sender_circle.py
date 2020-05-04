# Generated by Django 3.0.5 on 2020-05-03 23:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meets', '0004_auto_20200424_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatlog',
            name='sender_circle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chat_logs', to='meets.Circle', verbose_name='送信元サークル'),
        ),
    ]