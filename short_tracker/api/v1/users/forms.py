from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


class UploadFileForm(forms.Form):
    file = forms.ImageField()
