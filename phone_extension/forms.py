from django import forms
from .models import PhoneExtension

class PhoneExtensionForm(forms.ModelForm):
    class Meta:
        model = PhoneExtension
        fields = ['name', 'extension_number', 'full_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'extension_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Extension Number'}),
            'full_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Number (Optional)'}),
        }

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='Select a CSV file', widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.csv'}))
