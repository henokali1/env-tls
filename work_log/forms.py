from django import forms
from .models import WorkLog, Tag
import datetime

class WorkLogForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        initial=datetime.date.today
    )
    task_description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'autofocus': 'autofocus'}),
        label="Task Description"
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = WorkLog
        fields = ['date', 'task_description', 'tags']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'color']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.Select(attrs={'class': 'form-control'})
        }
