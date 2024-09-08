# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_video, name='upload_video'),
    path('pred/', views.PredictionResultsView.as_view(), name='prediction_results'),
]
