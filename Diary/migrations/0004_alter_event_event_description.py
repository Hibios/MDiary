# Generated by Django 3.2 on 2021-05-20 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Diary', '0003_auto_20210520_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_description',
            field=models.CharField(max_length=1000),
        ),
    ]
