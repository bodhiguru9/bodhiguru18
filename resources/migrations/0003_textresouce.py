# Generated by Django 4.2.4 on 2024-09-18 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0002_resource_thumbnail'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextResouce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
    ]