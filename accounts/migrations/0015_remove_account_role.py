# Generated by Django 4.2.4 on 2024-09-06 08:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_alter_account_role_alter_account_sub_org'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='role',
        ),
    ]