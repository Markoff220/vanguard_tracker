# Generated by Django 4.2.3 on 2023-07-06 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0006_delete_archive'),
    ]

    operations = [
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('type_habit', models.CharField(max_length=10)),
                ('question', models.CharField(max_length=50)),
                ('color', models.CharField(max_length=10)),
                ('frequency', models.CharField(max_length=20)),
                ('units', models.CharField(max_length=10)),
                ('target', models.IntegerField()),
                ('date_start', models.CharField(max_length=15)),
                ('date_finish', models.CharField(max_length=15)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.user')),
            ],
        ),
    ]
