from django import forms
from .models import Credential, System

class CredentialForm(forms.ModelForm):
    class Meta:
        model = Credential
        fields = ['system', 'location', 'description', 'username', 'password', 'ipv4', 'subnet_mask', 'gateway', 'remarks', 'image']

    def clean_ipv4(self):
        data = self.cleaned_data['ipv4']
        if data:
            data = data.strip()
        return data

    def clean_subnet_mask(self):
        data = self.cleaned_data['subnet_mask']
        if data:
            data = data.strip()
        return data

    def clean_gateway(self):
        data = self.cleaned_data['gateway']
        if data:
            data = data.strip()
        return data

class BulkImportForm(forms.Form):
    csv_file = forms.FileField(
        label='Select a CSV file',
        help_text='Ensure the file has the correct headers: System, Location, Description, Username, Password, IPv4, Subnet Mask, Gateway, Remarks'
    )
