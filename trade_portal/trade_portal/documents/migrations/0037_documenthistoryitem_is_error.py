# Generated by Django 2.2.10 on 2020-11-26 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0036_auto_20201118_0414'),
    ]

    operations = [
        migrations.AddField(
            model_name='documenthistoryitem',
            name='is_error',
            field=models.BooleanField(default=False),
        ),
    ]