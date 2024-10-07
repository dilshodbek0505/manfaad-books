# Generated by Django 5.1.1 on 2024-10-06 23:57

import phonenumber_field.modelfields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='Model id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('full_name', models.CharField(help_text="User's full name.", max_length=255)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text="User's phone number.", max_length=128, region='UZ', unique=True)),
                ('age', models.PositiveIntegerField(help_text="User's age.")),
                ('avatar', models.ImageField(default='default.jpg', help_text="User's avatar.", upload_to='users_avatar/')),
                ('is_premium', models.BooleanField(default=False, help_text='User is premium.')),
                ('is_staff', models.BooleanField(default=False, help_text='User is staff.')),
                ('is_deleted', models.BooleanField(default=False, help_text='User is deleted.')),
                ('is_superuser', models.BooleanField(default=False, help_text='User is superuser.')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
