from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
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
