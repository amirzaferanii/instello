# Generated by Django 5.1.1 on 2024-09-17 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='profile_pics')),
                ('bio', models.TextField(blank=True, null=True)),
                ('follower', models.PositiveIntegerField(default=0)),
                ('following', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
