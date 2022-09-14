from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('adm/', admin.site.urls),
    path('', include('account.urls')),
    path('', include('chat.urls')),

# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]
# urlpatterns += static(settings.STATIC_URL,document_root= settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)
