from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('prediction.urls')),
]

# Add this block conditionally if DEBUG is True
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static('/output_videos/', document_root=settings.BASE_DIR / 'output_videos')
    urlpatterns += static('/videos/', document_root=settings.BASE_DIR / 'videos')
