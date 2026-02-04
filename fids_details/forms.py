from django import forms
from .models import FidsDetail

class FidsDetailForm(forms.ModelForm):
    class Meta:
        model = FidsDetail
        fields = ['device_id', 'ip_address', 'mac_address', 'location']
        widgets = {
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Device ID'}),
            'ip_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'IP Address'}),
            'mac_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MAC Address'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
        }

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='Select a CSV file', widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.csv'}))
