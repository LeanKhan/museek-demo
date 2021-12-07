# Generated by Django 3.2.9 on 2021-12-07 14:21

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music', '0006_auto_20211207_1510'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='library',
        ),
        migrations.AddField(
            model_name='list',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='library', to='auth.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='list',
            name='created_at',
            field=models.DateTimeField(verbose_name=datetime.datetime(2021, 12, 7, 14, 20, 57, 372674, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='list',
            name='updated_at',
            field=models.DateTimeField(verbose_name=datetime.datetime(2021, 12, 7, 14, 20, 57, 372674, tzinfo=utc)),
        ),
    ]