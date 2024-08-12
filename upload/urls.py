from django.urls import path
from .views import upload_files, search

urlpatterns = [
    path('', upload_files, name='upload_files'),
    path('search/', search, name='search'),
]
