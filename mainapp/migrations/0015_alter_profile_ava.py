# Generated by Django 4.1.7 on 2023-07-30 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0014_profile_ava'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='ava',
            field=models.ImageField(default='/static/images/userlogodefault.jpg', upload_to='avatars'),
        ),
    ]
