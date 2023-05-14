from django.urls import path
from . views import upload, search_page

urlpatterns = [
    path('', upload, name='upload'),
    path('search', search_page, name='search_page'),
]
