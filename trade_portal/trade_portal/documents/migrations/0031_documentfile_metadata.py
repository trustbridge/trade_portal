# Generated by Django 2.2.10 on 2020-08-29 15:57

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0030_document_raw_certificate_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentfile',
            name='metadata',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict),
        ),
    ]
