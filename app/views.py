from typing import *
from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpRequest
from .forms import FileUploadForm, SearchPhraseForm
from .utils import upload_data, search_text
from asgiref.sync import async_to_sync

# Create your views here.


def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'home.html')


def api_home(request: HttpRequest) -> HttpResponse:
    return render(request, 'api_home.html')


def upload(request: HttpRequest) -> HttpResponse:

    if request.method == 'POST':

        # Get file from form data
        form_data = FileUploadForm(request.POST, request.FILES)
        if form_data.is_valid():
            # Save file in DynamoDB
            # Process the file in async thread
            file = form_data.files.get('file')
            upload_data(file)
            return redirect('search_page')
        return render(request, 'upload_form.html', {'form': form_data, 'info': 'Invalid form data'})
    form = FileUploadForm()

    return render(request, 'upload_form.html', {'form': form, 'info': ''})


def search_page(request: HttpRequest) -> HttpResponse:

    if request.method == 'POST':
        # Get search phrase from form data
        search_form = SearchPhraseForm(request.POST)
        # Search phrase using Elastic Search
        # Process the search in async thread
        print(search_form.is_valid())
        if search_form.is_valid():
            table_data = search_text(search_form.cleaned_data['search_phrase'])
            print(table_data)
            return render(request, 'search_page.html', {'data': table_data, 'search_form': search_form})
        return render(request, 'search_page.html', {'data': [], 'search_form': search_form})
    search_form = SearchPhraseForm()

    return render(request, 'search_page.html', {'data': [], 'search_form': search_form})
