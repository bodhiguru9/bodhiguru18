# Generated by Django 4.2.4 on 2024-10-05 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upgrade', '0010_upgrade_assessment_package'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='upgrade',
            name='assessment_package',
        ),
        migrations.AddField(
            model_name='upgrade',
            name='assessment_package',
            field=models.ManyToManyField(blank=True, default=1, to='upgrade.upgradeassessment'),
        ),
    ]