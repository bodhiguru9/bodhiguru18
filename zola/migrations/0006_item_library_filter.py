# Generated by Django 4.2.4 on 2024-09-20 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zola', '0005_alter_item_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='library_filter',
            field=models.CharField(default='filter', max_length=700),
        ),
    ]
