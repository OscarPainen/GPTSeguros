# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('cotizar/', views.ejecutar_cotizador, name='ejecutar_cotizador'),
    path('', views.RealizarCotizacion, name='Realizar_Cotizacion'),
]


   