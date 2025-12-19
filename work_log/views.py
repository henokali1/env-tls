import csv
import datetime
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from .models import WorkLog, Tag
from .forms import WorkLogForm, TagForm
from django.urls import reverse_lazy

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

        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        if tag_id and tag_id.strip():
            queryset = queryset.filter(tags=tag_id)
            
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

    if start_date:
        queryset = queryset.filter(date__gte=start_date)
    if end_date:
        queryset = queryset.filter(date__lte=end_date)
    if tag_id and tag_id.strip():
        queryset = queryset.filter(tags=tag_id)

    queryset = queryset.distinct()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="worklogs.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Task Description', 'Tags'])

    for log in queryset:
        tags = ", ".join([tag.name for tag in log.tags.all()])
        writer.writerow([log.date, log.task_description, tags])

    return response
