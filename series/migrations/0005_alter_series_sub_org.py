# Generated by Django 4.2.4 on 2024-09-06 08:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orgss', '0004_role1_suborg1_remove_role_suborg_remove_suborg_org'),
        ('series', '0004_itemseason_item_itemseason_season'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='sub_org',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orgss.suborg1'),
        ),
    ]
