from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.addItem),
    path('all/', views.getData),
    path('charge/', views.charge)
]