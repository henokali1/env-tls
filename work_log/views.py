import csv
import datetime
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from .models import WorkLog, Tag
from .forms import WorkLogForm, TagForm
from django.urls import reverse_lazy
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import WorkLogSerializer

class WorkLogAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = WorkLog.objects.all()

        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        tag = request.query_params.get('tag')

        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        if tag:
            queryset = queryset.filter(tags__id=tag)

        queryset = queryset.distinct().order_by('date')
        
        serializer = WorkLogSerializer(queryset, many=True)
        return Response(serializer.data)

class WorkLogCreateView(LoginRequiredMixin, CreateView):
    model = WorkLog
    form_class = WorkLogForm
    template_name = 'work_log/worklog_form.html'
    success_url = reverse_lazy('worklog_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class WorkLogListView(LoginRequiredMixin, ListView):
    model = WorkLog
    template_name = 'work_log/worklog_list.html'
    context_object_name = 'worklogs'
    paginate_by = 10 

    def get_paginate_by(self, queryset):
        if self.request.GET.get('show_all'):
            return None
        return self.paginate_by

    def get_queryset(self):
        queryset = WorkLog.objects.filter(user=self.request.user).order_by('-date', '-created_at').distinct()
        
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        tag_id = self.request.GET.get('tag')
        query = self.request.GET.get('q')

        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        if tag_id and tag_id.strip():
            queryset = queryset.filter(tags=tag_id)
        if query and query.strip():
            queryset = queryset.filter(task_description__icontains=query)
            
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        if 'form' not in context:
            context['form'] = WorkLogForm()
        return context

    def post(self, request, *args, **kwargs):
        form = WorkLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            form.save_m2m()
            return redirect('worklog_list')
        
        self.object_list = self.get_queryset()
        return self.render_to_response(self.get_context_data(form=form))

class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'work_log/tag_form.html'
    success_url = reverse_lazy('worklog_new')

def export_worklogs_csv(request):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)

    queryset = WorkLog.objects.filter(user=request.user).order_by('-date').distinct()
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    tag_id = request.GET.get('tag')
    query = request.GET.get('q')

    if start_date:
        queryset = queryset.filter(date__gte=start_date)
    if end_date:
        queryset = queryset.filter(date__lte=end_date)
    if tag_id and tag_id.strip():
        queryset = queryset.filter(tags=tag_id)
    if query and query.strip():
        queryset = queryset.filter(task_description__icontains=query)

    queryset = queryset.distinct()

    filename = "worklogs"
    if start_date and end_date:
        filename = f"worklogs_{start_date}_to_{end_date}"
    elif start_date:
        filename = f"worklogs_since_{start_date}"
    elif end_date:
        filename = f"worklogs_until_{end_date}"

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Task Description', 'Tags'])

    for log in queryset:
        tags = ", ".join([tag.name for tag in log.tags.all()])
        writer.writerow([log.date, log.task_description, tags])

    return response
