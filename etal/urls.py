from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('account.urls')),
    path('', include('chat.urls')),
    path('adm/', admin.site.urls),
    path('', include('home.urls')),
    path("", include("calendarapp.urls")),
    path("", include("researchnote.urls")),

# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root= settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)
