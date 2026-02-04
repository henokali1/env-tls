import csv
import io
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import FidsDetail
from .forms import FidsDetailForm, CSVUploadForm

def normalize_mac(mac):
    """Normalize MAC address to XX:XX:XX:XX:XX:XX format."""
    clean_mac = "".join(c for c in mac if c.isalnum()).upper()
    if len(clean_mac) == 12:
        return ":".join(clean_mac[i:i+2] for i in range(0, 12, 2))
    return mac.upper()

@login_required
def fids_list(request):
    details = FidsDetail.objects.all()
    # Pass all unique locations for filtering
    locations = FidsDetail.objects.values_list('location', flat=True).distinct().order_by('location')
    return render(request, 'fids_details/list.html', {
        'details': details,
        'locations': locations
    })

@login_required
def fids_manage(request):
    form = FidsDetailForm()
    csv_form = CSVUploadForm()

    if request.method == 'POST':
        if 'submit_single' in request.POST:
            form = FidsDetailForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.mac_address = normalize_mac(instance.mac_address)
                # Check for duplicates manually due to normalization
                if FidsDetail.objects.filter(mac_address=instance.mac_address).exists():
                    messages.error(request, f"MAC Address {instance.mac_address} already exists.")
                elif FidsDetail.objects.filter(device_id=instance.device_id).exists():
                    messages.error(request, f"Device ID {instance.device_id} already exists.")
                elif FidsDetail.objects.filter(ip_address=instance.ip_address).exists():
                    messages.error(request, f"IP Address {instance.ip_address} already exists.")
                else:
                    instance.save()
                    messages.success(request, 'FIDS detail added successfully.')
                    return redirect('fids_list')
        
        elif 'submit_csv' in request.POST:
            csv_form = CSVUploadForm(request.POST, request.FILES)
            if csv_form.is_valid():
                csv_file = request.FILES['csv_file']
                try:
                    decoded_file = csv_file.read().decode('utf-8-sig') # handle BOM if present
                    io_string = io.StringIO(decoded_file)
                    reader = csv.DictReader(io_string)
                    
                    added_count = 0
                    duplicate_count = 0
                    error_count = 0
                    errors = []

                    for row in reader:
                        # Map common variations of headers
                        device_id = row.get('Device ID') or row.get('device_id') or row.get('DeviceID')
                        ip_address = row.get('IP Address') or row.get('ip_address') or row.get('IP')
                        mac_address = row.get('MAC Address') or row.get('mac_address') or row.get('MAC')
                        location = row.get('Location') or row.get('location')

                        if not all([device_id, ip_address, mac_address, location]):
                            error_count += 1
                            continue
                        
                        mac_address = normalize_mac(mac_address)
                        
                        # Check duplicates
                        if FidsDetail.objects.filter(device_id=device_id).exists() or \
                           FidsDetail.objects.filter(ip_address=ip_address).exists() or \
                           FidsDetail.objects.filter(mac_address=mac_address).exists():
                            duplicate_count += 1
                            continue
                        
                        try:
                            FidsDetail.objects.create(
                                device_id=device_id,
                                ip_address=ip_address,
                                mac_address=mac_address,
                                location=location
                            )
                            added_count += 1
                        except Exception as e:
                            error_count += 1
                            errors.append(str(e))
                    
                    feedback = f"Successfully added: {added_count}. Duplicates found: {duplicate_count}. Errors: {error_count}."
                    if errors:
                        feedback += f" Last error: {errors[-1]}"
                    
                    if added_count > 0:
                        messages.success(request, feedback)
                    else:
                        messages.warning(request, feedback)
                    
                    return redirect('fids_list')
                except Exception as e:
                    messages.error(request, f'Error importing CSV: {e}')

    return render(request, 'fids_details/manage.html', {
        'form': form,
        'csv_form': csv_form
    })

@login_required
def fids_update(request, pk):
    detail = get_object_or_404(FidsDetail, pk=pk)
    if request.method == 'POST':
        form = FidsDetailForm(request.POST, instance=detail)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.mac_address = normalize_mac(instance.mac_address)
            # Check for duplicates (excluding self)
            if FidsDetail.objects.filter(mac_address=instance.mac_address).exclude(pk=pk).exists():
                messages.error(request, "MAC Address already exists.")
            elif FidsDetail.objects.filter(device_id=instance.device_id).exclude(pk=pk).exists():
                messages.error(request, "Device ID already exists.")
            elif FidsDetail.objects.filter(ip_address=instance.ip_address).exclude(pk=pk).exists():
                messages.error(request, "IP Address already exists.")
            else:
                instance.save()
                messages.success(request, 'FIDS detail updated successfully.')
                return redirect('fids_list')
    else:
        form = FidsDetailForm(instance=detail)
    
    return render(request, 'fids_details/edit.html', {'form': form, 'detail': detail})

@login_required
def fids_delete(request, pk):
    detail = get_object_or_404(FidsDetail, pk=pk)
    if request.method == 'POST':
        detail.delete()
        messages.success(request, 'FIDS detail deleted successfully.')
        return redirect('fids_list')
    return render(request, 'fids_details/delete_confirm.html', {'detail': detail})

def download_sample_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="fids_details_sample.csv"'

    writer = csv.writer(response)
    writer.writerow(['Device ID', 'IP Address', 'MAC Address', 'Location'])
    writer.writerow(['FIDS-001', '192.168.1.10', '68:27:37:01:23:46', 'Gate 1'])
    writer.writerow(['FIDS-002', '192.168.1.11', '68-27-37-01-23-47', 'Departure Hall'])
    writer.writerow(['FIDS-003', '192.168.1.12', '682737012348', 'Arrival Lounge'])

    return response
