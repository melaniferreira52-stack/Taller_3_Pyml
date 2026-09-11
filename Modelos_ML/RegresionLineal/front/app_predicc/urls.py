from django.urls import path
from . import views

urlpatterns = [
    path('', views.tasador, name='tasador'),
]