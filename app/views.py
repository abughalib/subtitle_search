from typing import *
from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpRequest
from .forms import FileUploadForm, SearchPhraseForm
from .utils import upload_video, search_text

# Create your views here.


def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'app/home.html')


def api_home(request: HttpRequest) -> HttpResponse:
    return render(request, 'app/api_home.html')


def upload(request: HttpRequest) -> HttpResponse:

    if request.method == 'POST':

        # Get file from form data
        form_data = FileUploadForm(request.POST, request.FILES)
        if form_data.is_valid():
            # Save file in DynamoDB
            # Process the file in async thread
            file = form_data.files.get('file')
            upload_video(file)
            return redirect('search_page')
        return render(request, 'app/upload_form.html', {'form': form_data, 'info': 'Invalid form data'})
    form = FileUploadForm()

    return render(request, 'app/upload_form.html', {'form': form, 'info': ''})


def search_page(request: HttpRequest) -> HttpResponse:

    if request.method == 'POST':
        # Get search phrase from form data
        search_form = SearchPhraseForm(request.POST)
        # Search phrase using Meilisearch
        # Process the search in async thread
        print(search_form.is_valid())
        if search_form.is_valid():
            table_data = search_text(search_form.cleaned_data['search_phrase'])
            if table_data:
                return render(request, 'app/search_page.html', {'data': table_data["hits"], 'search_form': search_form, 'time_taken': table_data["processingTimeMs"]})
            else:
                return render(request, 'app/search_page.html', {'data': [], 'search_form': search_form, 'info': 'No results found'})
        return render(request, 'app/search_page.html', {'data': [], 'search_form': search_form})
    search_form = SearchPhraseForm()

    return render(request, 'app/search_page.html', {'data': [], 'search_form': search_form})
