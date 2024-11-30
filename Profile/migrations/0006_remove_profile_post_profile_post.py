# Generated by Django 5.1.1 on 2024-09-17 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0005_remove_post_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='post',
        ),
        migrations.AddField(
            model_name='profile',
            name='post',
            field=models.ManyToManyField(blank=True, null=True, related_name='post', to='Profile.post'),
        ),
    ]
