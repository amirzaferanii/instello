# Generated by Django 5.1.1 on 2024-09-14 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='otp',
            options={'verbose_name': 'کد تایید ثبت نام', 'verbose_name_plural': 'کد های تایید ثبت نام'},
        ),
        migrations.AlterModelOptions(
            name='otpcode',
            options={'verbose_name': 'کد تایید', 'verbose_name_plural': 'کد های تایید'},
        ),
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics'),
        ),
        migrations.AddField(
            model_name='user',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='otp',
            name='code',
            field=models.SmallIntegerField(verbose_name='کد تایید'),
        ),
        migrations.AlterField(
            model_name='otp',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='ایمیل'),
        ),
        migrations.AlterField(
            model_name='otp',
            name='fullname',
            field=models.CharField(default='unknown', max_length=150, verbose_name='نام کامل'),
        ),
        migrations.AlterField(
            model_name='otp',
            name='phone',
            field=models.CharField(max_length=11, verbose_name='شماره تماس'),
        ),
        migrations.AlterField(
            model_name='otp',
            name='token',
            field=models.CharField(max_length=200, null=True, verbose_name='توکن'),
        ),
        migrations.AlterField(
            model_name='otpcode',
            name='code',
            field=models.SmallIntegerField(verbose_name='کد تایید'),
        ),
        migrations.AlterField(
            model_name='otpcode',
            name='phone',
            field=models.CharField(max_length=11, verbose_name='تلفن'),
        ),
        migrations.AlterField(
            model_name='otpcode',
            name='token',
            field=models.CharField(max_length=200, null=True, verbose_name='توکن'),
        ),
    ]