# Generated by Django 5.0 on 2023-12-11 10:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_customuser_created_at_customuser_mobile_location_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datescheduled', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule_created_by', to='api.customuser')),
                ('vehicles', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='User_vehicle', to='api.vehicle')),
            ],
        ),
    ]