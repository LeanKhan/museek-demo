# Generated by Django 3.2.9 on 2021-12-07 14:42

import datetime
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):

    dependencies = [
        ('music', '0008_auto_20211207_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='list',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
