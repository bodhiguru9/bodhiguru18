# Generated by Django 4.2.4 on 2024-09-06 08:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orgss', '0004_role1_suborg1_remove_role_suborg_remove_suborg_org'),
        ('assessments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessmenttype',
            name='suborg',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orgss.suborg1'),
        ),
    ]
