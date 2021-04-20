from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload', views.upload, name='upload'),
    path('file', views.file, name='file'),
    path('download_csv_template', views.download_csv_template),
]
