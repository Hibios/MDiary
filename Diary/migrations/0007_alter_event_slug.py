# Generated by Django 3.2 on 2021-05-24 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Diary', '0006_event_event_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=models.SlugField(default='djangodbmodelsfieldscharfield', max_length=250, unique_for_date='pub_date'),
        ),
    ]
