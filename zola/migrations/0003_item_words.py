# Generated by Django 5.1 on 2024-08-29 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zola', '0002_item_tags_suggestion_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='words',
            field=models.TextField(default='words'),
        ),
    ]
