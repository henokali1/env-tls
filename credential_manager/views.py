import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Credential, System, Location
from .forms import CredentialForm, BulkImportForm

def dashboard(request):
    return render(request, 'dashboard.html')


# System Views
class SystemListView(LoginRequiredMixin, ListView):
    model = System
    template_name = 'credential_manager/system_list.html'

class SystemCreateView(LoginRequiredMixin, CreateView):
    model = System
    fields = ['name']
    success_url = reverse_lazy('system_list')
    template_name = 'credential_manager/system_form.html'

class SystemUpdateView(LoginRequiredMixin, UpdateView):
    model = System
    fields = ['name']
    success_url = reverse_lazy('system_list')
    template_name = 'credential_manager/system_form.html'

class SystemDeleteView(LoginRequiredMixin, DeleteView):
    model = System
    success_url = reverse_lazy('system_list')
    template_name = 'credential_manager/system_confirm_delete.html'

# Location Views
class LocationListView(LoginRequiredMixin, ListView):
    model = Location
    template_name = 'credential_manager/location_list.html'

class LocationCreateView(LoginRequiredMixin, CreateView):
    model = Location
    fields = ['name']
    success_url = reverse_lazy('location_list')
    template_name = 'credential_manager/location_form.html'

class LocationUpdateView(LoginRequiredMixin, UpdateView):
    model = Location
    fields = ['name']
    success_url = reverse_lazy('location_list')
    template_name = 'credential_manager/location_form.html'

class LocationDeleteView(LoginRequiredMixin, DeleteView):
    model = Location
    success_url = reverse_lazy('location_list')
    template_name = 'credential_manager/location_confirm_delete.html'

# Credential Views
class CredentialListView(LoginRequiredMixin, ListView):
    model = Credential
    template_name = 'credential_manager/credential_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        system_id = self.request.GET.get('system')
        location_id = self.request.GET.get('location')

        if system_id:
            queryset = queryset.filter(system_id=system_id)
        
        if location_id:
            queryset = queryset.filter(location_id=location_id)

        if query:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(description__icontains=query) |
                Q(username__icontains=query) |
                Q(password__icontains=query) |
                Q(ipv4__icontains=query) |
                Q(subnet_mask__icontains=query) |
                Q(gateway__icontains=query) |
                Q(remarks__icontains=query) |
                Q(location__name__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['systems'] = System.objects.all()
        context['locations'] = Location.objects.all()
        return context

@login_required
def credential_manage(request):
    credentials = Credential.objects.all().order_by('-created')
    form = CredentialForm()
    bulk_form = BulkImportForm()
    
    # Use existing systems and locations for the dropdown in management if needed
    systems = System.objects.all()
    locations = Location.objects.all()
    
    if request.method == 'POST':
        if 'submit_single' in request.POST:
            form = CredentialForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Credential created successfully.')
                return redirect('credential_manage')
        elif 'submit_bulk' in request.POST:
            bulk_form = BulkImportForm(request.POST, request.FILES)
            if bulk_form.is_valid():
                csv_file = request.FILES['csv_file']
                try:
                    decoded_file = csv_file.read().decode('utf-8').splitlines()
                    reader = csv.DictReader(decoded_file)
                    count = 0
                    for row in reader:
                        row = {k.strip(): v for k, v in row.items() if k}
                        system_name = row.get('System')
                        if not system_name: continue
                        system, _ = System.objects.get_or_create(name=system_name)
                        
                        location_name = row.get('Location')
                        location = None
                        if location_name:
                            location, _ = Location.objects.get_or_create(name=location_name)

                        Credential.objects.create(
                            system=system,
                            location=location,
                            description=row.get('Description', ''),
                            username=row.get('Username'),
                            password=row.get('Password'),
                            ipv4=row.get('IPv4'),
                            subnet_mask=row.get('Subnet Mask'),
                            gateway=row.get('Gateway'),
                            remarks=row.get('Remarks', '')
                        )
                        count += 1
                    messages.success(request, f'Successfully imported {count} credentials.')
                    return redirect('credential_manage')
                except Exception as e:
                    messages.error(request, f'Error processing file: {e}')

    return render(request, 'credential_manager/manage.html', {
        'credentials': credentials,
        'form': form,
        'bulk_form': bulk_form,
        'systems': systems,
        'locations': locations
    })

class CredentialDetailView(LoginRequiredMixin, DetailView):
    model = Credential
    template_name = 'credential_manager/credential_detail.html'

class CredentialCreateView(LoginRequiredMixin, CreateView):
    model = Credential
    form_class = CredentialForm
    success_url = reverse_lazy('credential_manage')
    template_name = 'credential_manager/credential_form.html'

class CredentialUpdateView(LoginRequiredMixin, UpdateView):
    model = Credential
    form_class = CredentialForm
    success_url = reverse_lazy('credential_manage')
    template_name = 'credential_manager/credential_form.html'

class CredentialDeleteView(LoginRequiredMixin, DeleteView):
    model = Credential
    success_url = reverse_lazy('credential_manage')

@login_required
def download_sample_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="credential_import_sample.csv"'

    writer = csv.writer(response)
    writer.writerow(['System', 'Location', 'Description', 'Username', 'Password', 'IPv4', 'Subnet Mask', 'Gateway', 'Remarks'])
    writer.writerow(['Example System', 'Main Office', 'Web Server', 'admin', 'secret123', '192.168.1.10', '255.255.255.0', '192.168.1.1', 'Main production server'])
    
    return response

@login_required
def bulk_import(request):
    if request.method == 'POST':
        form = BulkImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'Please upload a CSV file.')
                return render(request, 'credential_manager/bulk_import.html', {'form': form})
            
            try:
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)
                count = 0
                for row in reader:
                    # Clean keys (remove BOM or spaces)
                    row = {k.strip(): v for k, v in row.items() if k}
                    
                    system_name = row.get('System')
                    if not system_name:
                        continue
                        
                    system, _ = System.objects.get_or_create(name=system_name)
                    
                    location_name = row.get('Location')
                    location = None
                    if location_name:
                        location, _ = Location.objects.get_or_create(name=location_name)
                    
                    Credential.objects.create(
                        system=system,
                        location=location,
                        description=row.get('Description', ''),
                        username=row.get('Username'),
                        password=row.get('Password'),
                        ipv4=row.get('IPv4'),
                        subnet_mask=row.get('Subnet Mask'),
                        gateway=row.get('Gateway'),
                        remarks=row.get('Remarks', '')
                    )
                    count += 1
                messages.success(request, f'Successfully imported {count} credentials.')
                return redirect('credential_manage')
            except Exception as e:
                messages.error(request, f'Error processing file: {e}')
    else:
        form = BulkImportForm()
    
    return render(request, 'credential_manager/bulk_import.html', {'form': form})
