from django import forms
from .models import *

class CustomUploadForm(forms.ModelForm):
    class Meta:
        model=user_upload
        fields =["image"]