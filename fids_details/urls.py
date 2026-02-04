from django.urls import path
from . import views

urlpatterns = [
    path('', views.fids_list, name='fids_list'),
    path('manage/', views.fids_manage, name='fids_manage'),
    path('update/<int:pk>/', views.fids_update, name='fids_update'),
    path('delete/<int:pk>/', views.fids_delete, name='fids_delete'),
    path('download-sample/', views.download_sample_csv, name='fids_download_sample'),
]
