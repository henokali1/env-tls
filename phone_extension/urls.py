from django.urls import path
from . import views

urlpatterns = [
    path('', views.phone_extension_list, name='phone_extension_list'),
    path('manage/', views.phone_extension_manage, name='phone_extension_manage'),
    path('<int:pk>/edit/', views.phone_extension_update, name='phone_extension_edit'),
    path('<int:pk>/delete/', views.phone_extension_delete, name='phone_extension_delete'),
    path('sample-csv/', views.download_sample_csv, name='phone_extension_sample_csv'),
]
