# Generated by Django 4.1.7 on 2023-07-15 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0012_remove_game_winner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='item',
        ),
    ]
