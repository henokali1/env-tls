from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from credential_manager.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('credentials/', include('credential_manager.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('work-logs/', include('work_log.urls')),
    path('phone-extensions/', include('phone_extension.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
