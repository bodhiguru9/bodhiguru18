# Generated by Django 4.2.4 on 2024-10-15 08:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0015_remove_assessmenttype_negative_marks_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='timer',
        ),
    ]