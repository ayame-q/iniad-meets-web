# Generated by Django 3.1.7 on 2021-04-16 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meets', '0008_auto_20210416_0156'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatlog',
            name='receive_user',
        ),
    ]
