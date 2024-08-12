from django.urls import path
from .views import upload_file, search



urlpatterns = [
    path('', upload_file, name='upload_files'),
    path('search/', search, name='search'),
]
