from django import forms


class FileUploadForm(forms.Form):
    file = forms.FileField(required=True, label='Upload File')


class SearchPhraseForm(forms.Form):
    search_phrase = forms.CharField(required=True, label='Search Phrase')