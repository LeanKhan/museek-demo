# Generated by Django 3.2.9 on 2021-12-07 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_auto_20211207_1036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='audio_file',
        ),
    ]