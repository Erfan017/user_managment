# Generated by Django 3.2.9 on 2021-11-13 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_profile_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='timestamp_created',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='timestamp_updated',
        ),
    ]