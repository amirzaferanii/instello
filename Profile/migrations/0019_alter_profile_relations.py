# Generated by Django 5.1.1 on 2024-09-21 16:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0018_profile_relations'),
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='relations',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='settings.relation'),
        ),
    ]
