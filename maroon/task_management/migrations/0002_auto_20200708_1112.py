# Generated by Django 3.0.8 on 2020-07-08 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, help_text='Profile picture', upload_to='avatars/'),
        ),
    ]