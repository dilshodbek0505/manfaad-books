# Generated by Django 5.1.1 on 2024-10-06 23:25

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VersionHistory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='Model id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('version', models.CharField(max_length=64, verbose_name='Version')),
                ('required', models.BooleanField(default=True, verbose_name='Required')),
            ],
            options={
                'verbose_name': 'Version history',
                'verbose_name_plural': 'Version histories',
            },
        ),
    ]
