from django.urls import path
from . import views

urlpatterns = [
    path('', views.CredentialListView.as_view(), name='credential_list'),
    path('manage/', views.credential_manage, name='credential_manage'),
    path('new/', views.CredentialCreateView.as_view(), name='credential_create'),
    path('<int:pk>/', views.CredentialDetailView.as_view(), name='credential_detail'),
    path('<int:pk>/edit/', views.CredentialUpdateView.as_view(), name='credential_update'),
    path('<int:pk>/delete/', views.CredentialDeleteView.as_view(), name='credential_delete'),
    path('import/', views.bulk_import, name='credential_import'),
    path('import/sample/', views.download_sample_csv, name='credential_sample_csv'),
    
    # System URLs
    path('systems/', views.SystemListView.as_view(), name='system_list'),
    path('systems/new/', views.SystemCreateView.as_view(), name='system_create'),
    path('systems/<int:pk>/edit/', views.SystemUpdateView.as_view(), name='system_update'),
    path('systems/<int:pk>/delete/', views.SystemDeleteView.as_view(), name='system_delete'),

    # Location URLs
    path('locations/', views.LocationListView.as_view(), name='location_list'),
    path('locations/new/', views.LocationCreateView.as_view(), name='location_create'),
    path('locations/<int:pk>/edit/', views.LocationUpdateView.as_view(), name='location_update'),
    path('locations/<int:pk>/delete/', views.LocationDeleteView.as_view(), name='location_delete'),
]
