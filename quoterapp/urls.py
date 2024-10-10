# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('cotizar/', views.ejecutar_cotizador, name='ejecutar_cotizador'),
    path('cotizacion_formulario/', views.RealizarCotizacion, name='Realizar_Cotizacion'),
]


   