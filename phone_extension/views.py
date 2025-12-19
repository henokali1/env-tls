import csv
import io
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from .models import PhoneExtension
from .forms import PhoneExtensionForm, CSVUploadForm

def phone_extension_list(request):
    extensions = PhoneExtension.objects.all()
    return render(request, 'phone_extension/list.html', {'extensions': extensions})

def phone_extension_manage(request):
    extensions = PhoneExtension.objects.all()
    form = PhoneExtensionForm()
    csv_form = CSVUploadForm()

    if request.method == 'POST':
        if 'submit_single' in request.POST:
            form = PhoneExtensionForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Phone extension created successfully.')
                return redirect('phone_extension_manage')
        elif 'submit_csv' in request.POST:
            csv_form = CSVUploadForm(request.POST, request.FILES)
            if csv_form.is_valid():
                csv_file = request.FILES['csv_file']
                try:
                    decoded_file = csv_file.read().decode('utf-8')
                    io_string = io.StringIO(decoded_file)
                    reader = csv.DictReader(io_string)
                    count = 0
                    for row in reader:
                        name = row.get('Name') or row.get('name')
                        ext = row.get('Extension Number') or row.get('EXT NO') or row.get('extension_number')
                        full = row.get('Full Number') or row.get('Full No') or row.get('full_number')
                        
                        if name and ext:
                            PhoneExtension.objects.create(
                                name=name,
                                extension_number=ext,
                                full_number=full or ''
                            )
                            count += 1
                    messages.success(request, f'{count} extensions imported successfully.')
                    return redirect('phone_extension_manage')
                except Exception as e:
                    messages.error(request, f'Error importing CSV: {e}')
    
    context = {
        'extensions': extensions,
        'form': form,
        'csv_form': csv_form,
    }
    return render(request, 'phone_extension/manage.html', context)

def phone_extension_update(request, pk):
    extension = get_object_or_404(PhoneExtension, pk=pk)
    if request.method == 'POST':
        form = PhoneExtensionForm(request.POST, instance=extension)
        if form.is_valid():
            form.save()
            messages.success(request, 'Phone extension updated successfully.')
            return redirect('phone_extension_manage')
    else:
        form = PhoneExtensionForm(instance=extension)
    
    return render(request, 'phone_extension/edit.html', {'form': form, 'extension': extension})

def phone_extension_delete(request, pk):
    extension = get_object_or_404(PhoneExtension, pk=pk)
    if request.method == 'POST':
        extension.delete()
        messages.success(request, 'Phone extension deleted successfully.')
        return redirect('phone_extension_manage')
    return render(request, 'phone_extension/delete_confirm.html', {'extension': extension})

def download_sample_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sample_extensions.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Extension Number', 'Full Number'])
    writer.writerow(['John Doe', '1001', '+1234567890'])
    writer.writerow(['Jane Smith', '1002', ''])

    return response
