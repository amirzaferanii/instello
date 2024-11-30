from django import forms

from Profile.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption', 'photo', 'comment_status']
