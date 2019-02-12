from django import forms
from .models import uploaded_software

class upload_software_form(forms.ModelForm):
    class Meta:
        model = uploaded_software
        fields = ('software_name', 'software_location',)