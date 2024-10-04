import tkinter as tk
from tkinter import ttk
from bci.bci_v25 import bci_cotizador, get_download_path
from renta.renta_v45 import renta_cotizador
from mapfre.mapfre_v25 import mapfre_cotizador
from hdi.hdi_v25 import hdi_cotizador
from sura.sura_v3 import sura_cotizador
from fid.fid_v1 import fid_cotizador

import time
import threading

# Función que simula una caja de estado para reemplazar los messageboxes
def mostrar_estado(mensaje):
    estado_label.config(text=mensaje)
    root.update_idletasks()

def ejecutar_con_reintentos(funcion_cotizador, nombre_cotizacion, ruta_descarga, datos_cotizacion, max_intentos=3):
    intentos = 0
    while intentos < max_intentos:
        try:
            funcion_cotizador(ruta_descarga, datos_cotizacion)
            mostrar_estado(f"Cotización {nombre_cotizacion} Completada")
            break  # Si la cotización fue exitosa, salimos del bucle
        except Exception as e:
            intentos += 1
            if intentos < max_intentos:
                mostrar_estado(f"Error en la cotización {nombre_cotizacion}. Reintentando... ({intentos}/{max_intentos})")
            else:
                mostrar_estado(f"Cotización {nombre_cotizacion} fallida tras {max_intentos} intentos. Error: {e}")

def ejecutar_en_hilo(cotizador_en_uso, nombre, ruta_descarga, datos_cotizacion):
    thread = threading.Thread(target=ejecutar_con_reintentos, args=(cotizador_en_uso, nombre, ruta_descarga, datos_cotizacion))
    thread.start()

# Función que realiza todas las cotizaciones en orden
def realizar_cotizacion():
    datos_cotizacion = {
        "nombre_asegurado": entry_nombre_asegurado.get(),
        "rut": entry_rut.get(),
        "patente": entry_patente.get(),
        "marca": entry_marca.get(),
        "modelo": entry_modelo.get(),
        "anio": entry_anio.get(),
    }

    ruta_descarga = get_download_path(datos_cotizacion)

    ejecutar_en_hilo(bci_cotizador, 'BCI', ruta_descarga, datos_cotizacion)
    time.sleep(5)

    ejecutar_en_hilo(renta_cotizador, 'RENTA', ruta_descarga, datos_cotizacion)
    time.sleep(5)

    ejecutar_en_hilo(fid_cotizador, 'FID', ruta_descarga, datos_cotizacion)
    time.sleep(5)

    try:
        ejecutar_en_hilo(mapfre_cotizador, 'Mapfre', ruta_descarga, datos_cotizacion)
        time.sleep(5)

        ejecutar_en_hilo(hdi_cotizador, 'HDI', ruta_descarga, datos_cotizacion)
        time.sleep(5)

        ejecutar_en_hilo(sura_cotizador, 'Sura', ruta_descarga, datos_cotizacion)
        time.sleep(5)
    except Exception as e:
        mostrar_estado(f"Error en la ejecución: {e}")
        root.quit()

# Función para centrar la ventana
def centrar_ventana(ancho, alto):
    ancho_pantalla = root.winfo_screenwidth()
    alto_pantalla = root.winfo_screenheight()
    x = (ancho_pantalla // 2) - (ancho // 2)
    y = (alto_pantalla // 2) - (alto // 2)
    root.geometry(f'{ancho}x{alto}+{x}+{y}')

# Crear ventana principal
root = tk.Tk()


root.title("Cotizador de Seguros - Profesional")
centrar_ventana(800, 600)

# Configurar el estilo
style = ttk.Style()
style.theme_use('clam')  # Tema más moderno
style.configure('TLabel', font=('Helvetica', 12), padding=5)
style.configure('TButton', font=('Helvetica', 10, 'bold'), padding=10)
style.configure('TEntry', padding=5)

# Frame principal para agrupar los widgets
frame_principal = ttk.Frame(root, padding="10 10 10 10")
frame_principal.grid(row=0, column=0, padx=20, pady=20)

# Etiquetas y entradas
ttk.Label(frame_principal, text="Nombre del Asegurado").grid(row=0, column=0, sticky="W", padx=10, pady=10)
entry_nombre_asegurado = ttk.Entry(frame_principal, width=25)
entry_nombre_asegurado.grid(row=0, column=1, padx=10, pady=10)

ttk.Label(frame_principal, text="RUT (sin puntos ni guion)").grid(row=1, column=0, sticky="W", padx=10, pady=10)
entry_rut = ttk.Entry(frame_principal, width=25)
entry_rut.grid(row=1, column=1, padx=10, pady=10)

ttk.Label(frame_principal, text="Patente").grid(row=2, column=0, sticky="W", padx=10, pady=10)
entry_patente = ttk.Entry(frame_principal, width=25)
entry_patente.grid(row=2, column=1, padx=10, pady=10)

ttk.Label(frame_principal, text="Marca").grid(row=3, column=0, sticky="W", padx=10, pady=10)
entry_marca = ttk.Entry(frame_principal, width=25)
entry_marca.grid(row=3, column=1, padx=10, pady=10)

ttk.Label(frame_principal, text="Modelo").grid(row=4, column=0, sticky="W", padx=10, pady=10)
entry_modelo = ttk.Entry(frame_principal, width=25)
entry_modelo.grid(row=4, column=1, padx=10, pady=10)

ttk.Label(frame_principal, text="Año").grid(row=5, column=0, sticky="W", padx=10, pady=10)
entry_anio = ttk.Entry(frame_principal, width=25)
entry_anio.grid(row=5, column=1, padx=10, pady=10)

# Botones para cotización completa
boton_cotizar_todas = ttk.Button(frame_principal, text="Realizar Cotización Completa", command=realizar_cotizacion)
boton_cotizar_todas.grid(row=6, column=0, columnspan=2, pady=20)

# Separador
ttk.Separator(frame_principal, orient='horizontal').grid(row=7, column=0, columnspan=2, sticky="ew", pady=10)

# Caja de estado
estado_label = ttk.Label(frame_principal, text="Estado: Esperando...", font=('Helvetica', 10), foreground="blue")
estado_label.grid(row=8, column=0, columnspan=2, pady=10)



# Crear botones para cotizar individualmente por aseguradora
boton_cotizar_bci = ttk.Button(root, text="Cotizar BCI", command=lambda: ejecutar_en_hilo(bci_cotizador, 'BCI', get_download_path({
    "nombre_asegurado": entry_nombre_asegurado.get(),
    "rut": entry_rut.get(),
    "patente": entry_patente.get(),
    "marca": entry_marca.get(),
    "modelo": entry_modelo.get(),
    "anio": entry_anio.get(),
}), {
    "nombre_asegurado": entry_nombre_asegurado.get(),
    "rut": entry_rut.get(),
    "patente": entry_patente.get(),
    "marca": entry_marca.get(),
    "modelo": entry_modelo.get(),
    "anio": entry_anio.get(),
}))
boton_cotizar_bci.grid(row=4, column=2, padx=10, pady=10)

boton_cotizar_renta = ttk.Button(root, text="Cotizar Renta", command=lambda: ejecutar_en_hilo(renta_cotizador, 'RENTA', get_download_path({
    "nombre_asegurado": entry_nombre_asegurado.get(),
    "rut": entry_rut.get(),
    "patente": entry_patente.get(),
    "marca": entry_marca.get(),
    "modelo": entry_modelo.get(),
    "anio": entry_anio.get(),
}), {
    "nombre_asegurado": entry_nombre_asegurado.get(),
    "rut": entry_rut.get(),
    "patente": entry_patente.get(),
    "marca": entry_marca.get(),
    "modelo": entry_modelo.get(),
    "anio": entry_anio.get(),
}))
boton_cotizar_renta.grid(row=4, column=3, padx=10, pady=10)

boton_cotizar_mapfre = ttk.Button(root, text="Cotizar Mapfre", command=lambda: ejecutar_en_hilo(mapfre_cotizador, 'Mapfre', get_download_path({
    "nombre_asegurado": entry_nombre_asegurado.get(),
    "rut": entry_rut.get(),
    "patente": entry_patente.get(),
    "marca": entry_marca.get(),
    "modelo": entry_modelo.get(),
    "anio": entry_anio.get(),
}), {
    "nombre_asegurado": entry_nombre_asegurado.get(),
    "rut": entry_rut.get(),
    "patente": entry_patente.get(),
    "marca": entry_marca.get(),
    "modelo": entry_modelo.get(),
    "anio": entry_anio.get(),
}))
boton_cotizar_mapfre.grid(row=5, column=2, padx=10, pady=10)

boton_cotizar_hdi = ttk.Button(root, text="Cotizar HDI", command=lambda: ejecutar_en_hilo(hdi_cotizador, 'HDI', get_download_path({
    "nombre_asegurado": entry_nombre_asegurado.get(),
    "rut": entry_rut.get(),
    "patente": entry_patente.get(),
    "marca": entry_marca.get(),
    "modelo": entry_modelo.get(),
    "anio": entry_anio.get(),
}), {
    "nombre_asegurado": entry_nombre_asegurado.get(),
    "rut": entry_rut.get(),
    "patente": entry_patente.get(),
    "marca": entry_marca.get(),
    "modelo": entry_modelo.get(),
    "anio": entry_anio.get(),
}))
boton_cotizar_hdi.grid(row=5, column=3, padx=10, pady=10)

boton_cotizar_sura = ttk.Button(root, text="Cotizar Sura", command=lambda: ejecutar_en_hilo(sura_cotizador, 'Sura', get_download_path({
    "nombre_asegurado": entry_nombre_asegurado.get(),
    "rut": entry_rut.get(),
    "patente": entry_patente.get(),
    "marca": entry_marca.get(),
    "modelo": entry_modelo.get(),
    "anio": entry_anio.get(),
}), {
    "nombre_asegurado": entry_nombre_asegurado.get(),
    "rut": entry_rut.get(),
    "patente": entry_patente.get(),
    "marca": entry_marca.get(),
    "modelo": entry_modelo.get(),
    "anio": entry_anio.get(),
}))
boton_cotizar_sura.grid(row=6, column=2, padx=10, pady=10)


boton_cotizar_fid = ttk.Button(root, text="Cotizar FID", command=lambda: ejecutar_en_hilo(fid_cotizador, 'FID', get_download_path({
    "nombre_asegurado": entry_nombre_asegurado.get(),
    "rut": entry_rut.get(),
    "patente": entry_patente.get(),
    "marca": entry_marca.get(),
    "modelo": entry_modelo.get(),
    "anio": entry_anio.get(),
}), {
    "nombre_asegurado": entry_nombre_asegurado.get(),
    "rut": entry_rut.get(),
    "patente": entry_patente.get(),
    "marca": entry_marca.get(),
    "modelo": entry_modelo.get(),
    "anio": entry_anio.get(),
}))
boton_cotizar_fid.grid(row=6, column=3, padx=10, pady=10)
# Iniciar el bucle de la interfaz
root.mainloop()
