# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.RealizarCotizacion, name='Realizar_Cotizacion'),
]


   