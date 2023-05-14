from typing import *
from django.shortcuts import render, HttpResponse
from django.http import HttpRequest
from .forms import FileUploadForm

# Create your views here.


def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'home.html')

def upload(request: HttpRequest) -> HttpResponse:

    if request.method == 'POST':
        
        # Get file from form data
        form_data = FileUploadForm(request.POST)
        print(form_data.is_valid())

        return HttpResponse('File uploaded')
    
    form = FileUploadForm()

    return render(request, 'upload_form.html', {'form': form})

def search_page(request: HttpRequest) -> HttpResponse:

    data = [
        {'file_name': '1.mp4',
         'video_time': '00:00:00',
         'subtitle_line': 'Hello World!'},
        {'file_name': '2.mp4',
            'video_time': '00:00:00',
            'subtitle_line': 'Hello World!'},
        {'file_name': '3.mp4',
            'video_time': '00:00:00',
            'subtitle_line': 'Hello World!'},
        {'file_name': '4.mp4',
            'video_time': '00:00:00',
            'subtitle_line': 'Hello World!'},
        {'file_name': '5.mp4',
            'video_time': '00:00:00',
            'subtitle_line': 'Hello World!'},
    ]

    return render(request, 'search_page.html', {'data': data})
