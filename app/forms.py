from django import forms

class FileUploadForm(forms.Form):
    file = forms.FileField(required=True, label='Upload File')