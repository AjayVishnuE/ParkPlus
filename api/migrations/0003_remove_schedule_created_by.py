# Generated by Django 5.0 on 2023-12-17 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_schedule_extratime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='created_by',
        ),
    ]
