from django.urls import path
from .views import WorkLogCreateView, WorkLogListView, TagCreateView, export_worklogs_csv, WorkLogAPIView

urlpatterns = [
    path('new/', WorkLogCreateView.as_view(), name='worklog_new'),
    path('', WorkLogListView.as_view(), name='worklog_list'),
    path('tags/new/', TagCreateView.as_view(), name='tag_new'),
    path('export/', export_worklogs_csv, name='worklog_export'),
    path('api/logs/', WorkLogAPIView.as_view(), name='worklog_api'),
]
