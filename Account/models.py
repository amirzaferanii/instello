from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.text import slugify
from Profile.models import Profile, Follow


class MyUserManager(BaseUserManager):
    def create_user(self, phone, email=None, username=None, fullname=None, password=None):

        if not phone:
            raise ValueError("Users must have an phone address")

        user = self.model(phone=phone, fullname=fullname, username=username, email=email)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, fullname,username, password=None):

        user = self.create_user(phone,password=password, username=username ,fullname=fullname)
        user.is_admin = True
        Profile.objects.create(user=user)
        Follow.objects.get_or_create(user=user)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="آدرس ایمیل",max_length=255,null=True,blank=True)
    phone = models.CharField(verbose_name="شماره تلفن",max_length=11,unique=True,)
    fullname = models.CharField(verbose_name="نام کامل",max_length=255)
    username = models.CharField(max_length=255, unique=True,null=True,blank=True, verbose_name='نام کاربری')
    slug = models.SlugField(unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True,verbose_name='فعال')
    is_admin = models.BooleanField(default=False,verbose_name='ادمین')


    objects = MyUserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ['fullname','username']

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.phone

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super(User, self).save(*args, **kwargs)



    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Otp(models.Model):
    token = models.CharField(max_length=200,null=True , verbose_name='توکن')
    phone = models.CharField(max_length=11, verbose_name='شماره تماس')
    fullname = models.CharField(max_length=150,default='unknown',verbose_name='نام کامل')
    email = models.EmailField(null=True,blank=True, verbose_name='ایمیل')
    code = models.SmallIntegerField(verbose_name='کد تایید')
    expiration_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.phone

    class Meta:
        unique_together = ['phone', 'code']
        verbose_name_plural = 'کد های تایید ثبت نام'
        verbose_name = 'کد تایید ثبت نام'


class OtpCode(models.Model):
    code = models.SmallIntegerField(verbose_name='کد تایید')
    token = models.CharField(max_length=200, null=True, verbose_name='توکن')
    phone = models.CharField(max_length=11, verbose_name='تلفن')

    def __str__(self):
        return self.phone

    class Meta:
        unique_together = ['phone', 'code']
        verbose_name_plural = 'کد های تایید'
        verbose_name = 'کد تایید'



