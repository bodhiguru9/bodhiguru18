# Generated by Django 4.2.4 on 2024-10-01 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orgss', '0014_remove_org_upgrade_expiry'),
    ]

    operations = [
        migrations.AddField(
            model_name='org',
            name='expires_on',
            field=models.DateField(blank=True, null=True),
        ),
    ]
