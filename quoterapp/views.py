from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .forms import CotizacionForm
import logging
from selenium_gpt import cotizar as cotizador
# Create your views here.
import subprocess

def ejecutar_cotizador(request):
    if request.method == 'GET':
        try:
            # Ejecutar el script cotizador.py
            resultado = subprocess.run(['python3', 'cotizador.py'], capture_output=True, text=True)

            # Retornar la salida del script como respuesta
            return JsonResponse({'status': 'success', 'output': resultado.stdout})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'fail', 'message': 'Método no permitido'})

# Cotizacion Con Formulario
from .forms import CotizacionForm
logger = logging.getLogger(__name__)

def RealizarCotizacion(request):
    if request.method == 'POST':
        form = CotizacionForm(request.POST)
        if form.is_valid():
            try:
                # Procesar los datos de la cotización
                datos_cotizacion = {
                    'nombre_asegurado': form.cleaned_data['nombre_cliente'],
                    'rut': form.cleaned_data['rut_cliente'],
                    'marca': form.cleaned_data['marca_vehiculo'],
                    'modelo': form.cleaned_data['modelo_vehiculo'],
                    'patente': form.cleaned_data['license_plate'],
                    'anio': str(form.cleaned_data['año_vehiculo']),  # Convertir a string
                }
                
                logger.debug(f"Datos de cotización preparados: {datos_cotizacion}")
                
                # Llamar a la función cotizar
                
                cotizador.cotizar(datos_cotizacion)

                return HttpResponse(f"Resultado de la cotización: ok")
            
            except Exception as e:
                logger.error(f"Error durante la cotización: {str(e)}", exc_info=True)
                return HttpResponse(f"Error al procesar la cotización: {str(e)}", status=500)
    else:
        form = CotizacionForm()

    return render(request, 'quoterapp/cotizacion_form.html', {'form': form})