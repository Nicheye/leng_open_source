# Generated by Django 4.1.7 on 2023-08-16 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0018_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='background',
            field=models.ImageField(default=models.ImageField(default='/static/images/userlogodefault.jpg', upload_to='avatars'), upload_to='backgrounds'),
        ),
    ]
