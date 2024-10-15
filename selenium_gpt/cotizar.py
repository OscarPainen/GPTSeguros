from .bci import bci_cotizador, get_download_path
from .renta import renta_cotizador
from .mapfre import mapfre_cotizador
from .hdi import hdi_cotizador
from .sura import sura_cotizador
from .fid import fid_cotizador

import time
import threading

def ejecutar_en_hilo(cotizador_en_uso, nombre, ruta_descarga, datos_cotizacion):
    thread = threading.Thread( args=(cotizador_en_uso, nombre, ruta_descarga, datos_cotizacion))
    thread.start()


def cotizar(datos_cotizacion): # faltan: uso y tipo
    #ruta_descarga = get_download_path(datos_cotizacion)
    #bci_cotizador(get_download_path(datos_cotizacion),datos_cotizacion)
    mapfre_cotizador(get_download_path(datos_cotizacion),datos_cotizacion)
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