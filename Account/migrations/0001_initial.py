# Generated by Django 5.1.1 on 2024-09-14 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='آدرس ایمیل')),
                ('phone', models.CharField(max_length=11, unique=True, verbose_name='شماره تلفن')),
                ('fullname', models.CharField(max_length=255, verbose_name='نام کامل')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('is_admin', models.BooleanField(default=False, verbose_name='ادمین')),
            ],
            options={
                'verbose_name': 'کاربر',
                'verbose_name_plural': 'کاربران',
            },
        ),
        migrations.CreateModel(
            name='Otp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=200, null=True)),
                ('phone', models.CharField(max_length=11)),
                ('fullname', models.CharField(default='unknown', max_length=150)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('code', models.SmallIntegerField()),
                ('expiration_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'unique_together': {('phone', 'code')},
            },
        ),
        migrations.CreateModel(
            name='OtpCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.SmallIntegerField()),
                ('token', models.CharField(max_length=200, null=True)),
                ('phone', models.CharField(max_length=11)),
            ],
            options={
                'unique_together': {('phone', 'code')},
            },
        ),
    ]
