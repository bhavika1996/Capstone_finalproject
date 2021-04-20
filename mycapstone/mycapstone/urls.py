from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload', views.upload, name='upload'),
    path('file', views.file, name='file'),
    path('download_csv_template', views.download_csv_template),

    path('uplaod_csv', views.uplaod_csv),
    path('predict', views.predict, name='predict'),
    path('predict_post', views.predict_post, name="predict_post")
]
