# Generated by Django 3.1.7 on 2021-04-06 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calls', '0013_auto_20210406_1449'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='callrecord',
            name='duration',
        ),
    ]
