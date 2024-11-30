
from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('Account.urls')),
    path('', include('Profile.urls')),
    path('settings/', include('settings.urls')),
    path('chat/', include('chatuser.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
