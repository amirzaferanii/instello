# Generated by Django 5.1.1 on 2024-09-28 18:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0019_alter_profile_relations'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='Profile.profile'),
            preserve_default=False,
        ),
    ]