from django.db import models

from settings.models import Relation



class Profile(models.Model):
    user = models.ForeignKey('Account.User', on_delete=models.CASCADE, related_name='profiles')
    photo = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    working_at = models.CharField(max_length=150, null=True, blank=True)
    relations = models.ForeignKey(Relation, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{str(self.user)}'


class Post(models.Model):
    user = models.ForeignKey('Account.User', on_delete=models.CASCADE, related_name='post')
    photo = models.ImageField(upload_to='Post_pics', verbose_name='تصویر')
    caption = models.TextField(null=True, blank=True, verbose_name='کپشن')
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    comment_status = models.BooleanField(default=False, verbose_name='فعال سازی کامنت')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return f'{self.photo} - {self.caption}'



class Like(models.Model):
    user = models.ForeignKey('Account.User', on_delete=models.CASCADE)
    user_profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.post}'


class Comment(models.Model):
    user = models.ForeignKey('Account.User', on_delete=models.CASCADE, related_name='comments_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.post}'

class Follow(models.Model):
    user = models.ForeignKey('Account.User', on_delete=models.CASCADE, related_name='following_users', blank=True, null=True)
    followers = models.ManyToManyField('Account.User', related_name='followers', blank=True)
    following = models.ManyToManyField('Account.User', related_name='following', blank=True)

    def __str__(self):
        return str(self.user)






