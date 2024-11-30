from django.contrib import admin

from Profile.models import Profile, Post, Follow, Like, Comment

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')

admin.site.register(Post)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'parent', 'created')