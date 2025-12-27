from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from credential_manager.views import dashboard

from django.views.generic import TemplateView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('credentials/', include('credential_manager.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('work-logs/', include('work_log.urls')),
    path('phone-extensions/', include('phone_extension.urls')),
    path('manifest.json', TemplateView.as_view(template_name='manifest.json', content_type='application/json'), name='manifest.json'),
    path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/javascript'), name='sw_js'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
