# Generated by Django 4.2.4 on 2024-10-12 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0008_assessmentresult_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option',
            name='option_image',
            field=models.ImageField(blank=True, null=True, upload_to='media/option/option_image'),
        ),
    ]
