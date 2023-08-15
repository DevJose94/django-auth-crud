from django import forms
from .models import tasks

class TaskForm(forms.ModelForm):
    class Meta:
        model = tasks
        fields = ['title', 'description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
            'important': forms.CheckboxInput(attrs={'class':'form-check-input m-auto'}),
        }