# Generated by Django 4.1 on 2022-10-05 04:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=300)),
                ('password', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('enabled', models.BooleanField()),
                ('user_role_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.userrole')),
            ],
        ),
        migrations.CreateModel(
            name='LogPath',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=200)),
                ('enabled', models.BooleanField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.user')),
            ],
        ),
    ]