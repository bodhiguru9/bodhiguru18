# Generated by Django 4.2.4 on 2024-09-05 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_remove_userprofile_noscenarios_attempted_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='scenarios_attempted',
            field=models.IntegerField(),
        ),
    ]