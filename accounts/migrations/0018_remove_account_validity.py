# Generated by Django 4.2.4 on 2024-09-09 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_userprofile_active_userprofile_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='validity',
        ),
    ]