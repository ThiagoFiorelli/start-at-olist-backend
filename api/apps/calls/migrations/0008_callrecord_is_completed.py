# Generated by Django 3.1.7 on 2021-04-05 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calls', '0007_auto_20210405_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='callrecord',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]
