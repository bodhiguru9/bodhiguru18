# Generated by Django 4.2.4 on 2024-09-17 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedback',
            old_name='feedback',
            new_name='description',
        ),
        migrations.AddField(
            model_name='feedback',
            name='contact_number',
            field=models.CharField(default=1234567890, max_length=15),
        ),
    ]