# Generated by Django 3.2 on 2021-05-24 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Diary', '0009_alter_event_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, null=True, unique_for_date='pub_date'),
        ),
    ]
