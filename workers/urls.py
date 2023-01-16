from django.conf.urls import include
from django.contrib import admin
from django.urls import path
import attendance
from django.conf import settings
from django.conf.urls.static import static

handler404 = 'attendance.views.custom_page_not_found_view'
handler500 = 'attendance.views.custom_error_view'
handler403 = 'attendance.views.custom_permission_denied_view'
handler400 = 'attendance.views.custom_bad_request_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('attendance.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
