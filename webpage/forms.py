from django import forms
from .models import linux_software

class linux_upload_software_form(forms.ModelForm):
    class Meta:
        model = linux_software
        fields = ('linux_software_name', 'linux_software_location',)