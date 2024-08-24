# Generated by Django 5.1 on 2024-08-24 06:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('competency', '0001_initial'),
        ('orgss', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('suggestion_text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=700)),
                ('item_description', models.CharField(blank=True, max_length=300, null=True)),
                ('item_video', models.URLField(blank=True, null=True)),
                ('item_background', models.FileField(blank=True, null=True, upload_to='media/item/item_background')),
                ('item_answer', models.TextField(blank=True, null=True)),
                ('item_emotion', models.TextField(blank=True, null=True)),
                ('item_answercount', models.IntegerField(default=0)),
                ('category', models.CharField(blank=True, default='Personal', max_length=256)),
                ('thumbnail', models.FileField(blank=True, null=True, upload_to='media/item/thumbnail')),
                ('item_gender', models.CharField(choices=[('female', 'Female'), ('male', 'Male'), ('all', 'All')], default='all', max_length=30)),
                ('item_type', models.CharField(choices=[('simulation', 'Simulation'), ('email', 'Email')], default='simulation', max_length=30)),
                ('scenario_type', models.CharField(choices=[('sales', 'Sales'), ('customer_service', 'Customer Service'), ('interview', 'Interview')], default='sales', max_length=30)),
                ('coming_across_as', models.CharField(blank=True, max_length=250, null=True)),
                ('level', models.IntegerField(default=1)),
                ('expert', models.URLField(blank=True, null=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('is_live', models.BooleanField(default=False)),
                ('competencys', models.ManyToManyField(blank=True, to='competency.competency')),
                ('role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seanrole', to='orgss.role')),
            ],
        ),
        migrations.CreateModel(
            name='ItemResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('score', models.IntegerField(default=0)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zola.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
