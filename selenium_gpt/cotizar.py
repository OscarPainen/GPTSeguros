from .bci import bci_cotizador
from .renta import renta_cotizador
from .mapfre import mapfre_cotizador
from .hdi import hdi_cotizador
from .sura import sura_cotizador
from .fid import fid_cotizador

import time
import threading
import os 
import datetime

# Obtener Path
def get_root_path():
    """Obtiene la ruta raíz del proyecto a partir del archivo actual."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_download_path(data_cliente):
    """Devuelve la ruta de descarga personalizada según el cliente, en la raíz del proyecto."""
    root_path = get_root_path()
    folder_name = f"{data_cliente['nombre_asegurado']}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    download_path = os.path.join(root_path, folder_name)

    if not os.path.exists(download_path):
        os.makedirs(download_path)

    return download_path


def ejecutar_en_hilo(cotizador_en_uso, nombre, ruta_descarga, datos_cotizacion):
    thread = threading.Thread( args=(cotizador_en_uso, nombre, ruta_descarga, datos_cotizacion))
    thread.start()


def cotizar(datos_cotizacion): # faltan: uso y tipo
    #ruta_descarga = get_download_path(datos_cotizacion)
    #bci_cotizador(get_download_path(datos_cotizacion),datos_cotizacion)
    bci_cotizador(get_download_path(datos_cotizacion),datos_cotizacion)
    """
    ruta_descarga = get_download_path(datos_cotizacion)

    ejecutar_en_hilo(bci_cotizador, 'BCI', ruta_descarga, datos_cotizacion)
    time.sleep(5)

    ejecutar_en_hilo(renta_cotizador, 'RENTA', ruta_descarga, datos_cotizacion)
    time.sleep(5)

    ejecutar_en_hilo(fid_cotizador, 'FID', ruta_descarga, datos_cotizacion)
    time.sleep(5)

    ejecutar_en_hilo(mapfre_cotizador, 'Mapfre', ruta_descarga, datos_cotizacion)
    time.sleep(5)

    ejecutar_en_hilo(hdi_cotizador, 'HDI', ruta_descarga, datos_cotizacion)
    time.sleep(5)

    ejecutar_en_hilo(sura_cotizador, 'Sura', ruta_descarga, datos_cotizacion)
    time.sleep(5)
    """
    return get_download_path(datos_cotizacion)