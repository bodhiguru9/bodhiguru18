# Generated by Django 4.2.4 on 2024-09-06 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orgss', '0006_rename_name_suborg1_name1_alter_suborg1_org'),
    ]

    operations = [
        migrations.RenameField(
            model_name='suborg1',
            old_name='name1',
            new_name='name',
        ),
    ]
