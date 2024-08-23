# Generated by Django 5.1 on 2024-08-23 04:15

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orgss', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=25, unique=True)),
                ('email', models.EmailField(max_length=70, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now_add=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superadmin', models.BooleanField(default=False)),
                ('user_role', models.CharField(choices=[('super_admin', 'Super Admin'), ('admin', 'Admin'), ('user', 'User')], default='user', max_length=20)),
                ('is_email_confirmed', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('org', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orgss.org')),
                ('role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orgss.role')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmailConfirmationToken',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reset_password_token', models.CharField(blank=True, default='', max_length=50)),
                ('reset_password_expire', models.DateTimeField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quizzes_attempted', models.IntegerField(default=1)),
                ('quiz_score', models.IntegerField(default=1)),
                ('quizzes_streak', models.IntegerField(default=1)),
                ('scenarios_attempted', models.IntegerField(default=1)),
                ('scenarios_attempted_score', models.TextField(blank=True, default='', null=True)),
                ('jadu_attempted', models.IntegerField(blank=True, default=1, null=True)),
                ('jadu_asked', models.IntegerField(blank=True, default=1, null=True)),
                ('bookmarks', models.CharField(blank=True, max_length=300, null=True)),
                ('gender', models.CharField(blank=True, max_length=10, null=True)),
                ('user_scenario_saved', models.CharField(default='', max_length=250)),
                ('level', models.IntegerField(default=1)),
                ('city', models.CharField(default='', max_length=250)),
                ('user_powerwords', models.TextField(default='')),
                ('user_weakwords', models.TextField(default='')),
                ('scenario_attempt_pw', models.TextField(default='')),
                ('scenario_attempt_ww', models.TextField(default='')),
                ('pw_competency', models.CharField(default='pw', max_length=250)),
                ('ww_competency', models.CharField(default='ww', max_length=250)),
                ('competency_score', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
