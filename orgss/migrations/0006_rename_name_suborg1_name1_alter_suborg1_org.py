# Generated by Django 4.2.4 on 2024-09-06 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orgss', '0005_delete_role_suborg1_org_role1_suborg_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='suborg1',
            old_name='name',
            new_name='name1',
        ),
        migrations.AlterField(
            model_name='suborg1',
            name='org',
            field=models.ForeignKey(default=7, on_delete=django.db.models.deletion.CASCADE, related_name='org', to='orgss.org'),
        ),
    ]