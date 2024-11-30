from django.urls import path
from . import views

app_name = 'settings'

urlpatterns = [

    path('', views.SettingsView.as_view(), name='settings'),
    path('profile', views.ProfileUpdateView.as_view(), name='profile'),
]

