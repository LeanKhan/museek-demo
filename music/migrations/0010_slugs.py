# Generated by Django 3.2.9 on 2021-12-16 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0009_auto_20211207_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='slug',
            field=models.SlugField(null=True),
        ),
        migrations.AddField(
            model_name='song',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]