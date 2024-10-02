# Generated by Django 4.2.4 on 2024-10-02 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zola', '0009_alter_item_library_filter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='library_filter',
            field=models.CharField(choices=[('team player', 'Team Player'), ('sales', 'Sales'), ('will stick or not', 'Will Stick or Not'), ('handling customers', 'Handling Customers'), ('managing people', 'Managing People')], default='sales', max_length=30),
        ),
    ]
