# Generated by Django 3.1.7 on 2021-04-20 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meets', '0015_auto_20210420_0951'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='archive_url',
            field=models.URLField(blank=True, null=True, verbose_name='アーカイブURL'),
        ),
        migrations.AddField(
            model_name='status',
            name='streaming_url',
            field=models.URLField(blank=True, null=True, verbose_name='ストリーミングURL'),
        ),
    ]