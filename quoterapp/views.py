from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .forms import CotizacionForm
import logging
from selenium_gpt import cotizar as cotizador
# Create your views here.
# Cotizacion Con Formulario

from .forms import CotizacionForm
logger = logging.getLogger(__name__)

from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .forms import CotizacionForm
import logging
import zipfile
import os
import io
from selenium_gpt import cotizar as cotizador

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
                
                # Llamar a la función cotizar y obtener la ruta de la carpeta
                FolderPath = cotizador.cotizar(datos_cotizacion)
                
                # Crear archivo ZIP en memoria
                zip_buffer = io.BytesIO()
                
                with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                    # Agregar todos los archivos de la carpeta al ZIP
                    for foldername, subfolders, filenames in os.walk(FolderPath):
                        for filename in filenames:
                            file_path = os.path.join(foldername, filename)
                            zip_file.write(file_path, os.path.relpath(file_path, FolderPath))
                
                # Preparar el archivo ZIP para ser descargado
                zip_buffer.seek(0)
                response = HttpResponse(zip_buffer, content_type='application/zip')
                response['Content-Disposition'] = 'attachment; filename="CotizacionesCompletas.zip"'

                return response
            
            except Exception as e:
                logger.error(f"Error durante la cotización: {str(e)}", exc_info=True)
                return HttpResponse(f"Error al procesar la cotización: {str(e)}", status=500)
    else:
        form = CotizacionForm()

    return render(request, 'quoterapp/cotizacion_form.html', {'form': form})
