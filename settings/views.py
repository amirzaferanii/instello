
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import UpdateView, TemplateView
from .models import Relation
from Profile.models import Profile
from django.contrib import messages


class SettingsView(View):
    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        relation = Relation.objects.all()
        return render(request, 'settings/general_settings.html',
                      context={'user': user, 'profile': profile, 'relation': relation})

    def post(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        relation, fullname, email, working, bio = request.POST.get('relationship'), request.POST.get('fullname'), request.POST.get('email'), request.POST.get('working'), request.POST.get('bio')
        profile.relations_id = relation
        user.fullname = fullname
        user.email = email
        profile.working_at = working
        profile.bio = bio
        profile.save()
        user.save()
        messages.success(request, 'Your information has been successfully changed')
        return redirect('settings:settings')





class ProfileUpdateView(View):
    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        return render(request, 'settings/profile_photo.html',context={'user': user, 'profile': profile})

    def post(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        photo = request.FILES.get('profile_picture')
        profile.photo = photo
        profile.save()
        messages.success(request, 'Your profile has been updated!')
        return redirect('settings:settings')