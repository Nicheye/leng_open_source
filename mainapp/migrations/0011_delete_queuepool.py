# Generated by Django 4.1.7 on 2023-07-19 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0010_profile_in_queue_queuepool'),
    ]

    operations = [
        migrations.DeleteModel(
            name='QueuePool',
        ),
    ]
