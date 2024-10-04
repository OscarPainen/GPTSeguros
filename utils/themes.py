import tkinter as tk
from tkinter import ttk
from bci.bci_v3 import bci_cotizador, get_download_path
from renta.renta_v45 import renta_cotizador
from mapfre.mapfre_v25 import mapfre_cotizador
from hdi.hdi_v25 import hdi_cotizador
from sura.v4 import sura_cotizador
from fid.fid_v1 import fid_cotizador
import queue
import time
import threading

# Función que simula una caja de estado para reemplazar los messageboxes
def mostrar_estado(mensaje):
    estado_label.config(text=mensaje)
    root.update_idletasks()
# ----------- Ejecucion en orden ----------------

def ejecutar_con_reintentos(funcion_cotizador, nombre_cotizacion, ruta_descarga, datos_cotizacion, max_intentos=2):
    intentos = 0
    while intentos < max_intentos:
        try:
            funcion_cotizador(ruta_descarga, datos_cotizacion)
            mostrar_estado(f"Cotización {nombre_cotizacion} Completada")
            break
        except Exception as e:
            intentos += 1
            if intentos < max_intentos:
                mostrar_estado(f"Error en la cotización {nombre_cotizacion}. Reintentando... ({intentos}/{max_intentos})")
            else:
                mostrar_estado(f"Cotización {nombre_cotizacion} fallida tras {max_intentos} intentos. Error: {e}")

def procesar_cola(q):
    while not q.empty():
        cotizador, nombre, ruta_descarga, datos_cotizacion = q.get()
        ejecutar_con_reintentos(cotizador, nombre, ruta_descarga, datos_cotizacion)
        q.task_done()  # Marca la tarea como completada

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

    q = queue.Queue()

    # Agregar cotizadores a la cola
    #q.put((mapfre_cotizador, 'Mapfre', ruta_descarga, datos_cotizacion))

    q.put((bci_cotizador, 'BCI', ruta_descarga, datos_cotizacion))
    q.put((renta_cotizador, 'RENTA', ruta_descarga, datos_cotizacion))
    q.put((fid_cotizador, 'FID', ruta_descarga, datos_cotizacion))
    q.put((sura_cotizador, 'Sura', ruta_descarga, datos_cotizacion))
    q.put((hdi_cotizador, 'HDI', ruta_descarga, datos_cotizacion))

    # Procesar la cola
    procesar_cola(q)

# -------------------- ventana ----------------------------
# Función para centrar la ventana
def centrar_ventana(ancho, alto):
    root.update_idletasks()
    ancho_pantalla = root.winfo_screenwidth()
    alto_pantalla = root.winfo_screenheight()
    x = (ancho_pantalla // 2) - (ancho // 2)
    y = (alto_pantalla // 2) - (alto // 2)
    root.geometry(f'{ancho}x{alto}+{x}+{y}')

# Crear ventana principal
root = tk.Tk()
root.title("GPTSeguros - Vehiculos")
centrar_ventana(600, 800)

# Configurar el estilo
style = ttk.Style()
#print(style.theme_names())

style.theme_use('aqua')  # Tema más moderno
style.configure('Heading.TLabel', font=('Helvetica', 16, 'bold'), foreground='darkblue')
style.configure('TLabel', font=('Helvetica', 12), padding=5)
style.configure('TButton', font=('Helvetica', 10, 'bold'), padding=10)
style.configure('TEntry', padding=5)
style.configure('TFrame', padding=10)
style.configure('TButton', font=('Arial', 12, 'bold'), padding=10, relief='flat')
style.map('TButton', background=[('active', 'lightblue'), ('!disabled', 'white')], foreground=[('active', 'black')])
style.configure('Pressed.TButton', font=('Arial', 12, 'bold'), padding=10, relief='flat')
style.map('Pressed.TButton', background=[('pressed', 'darkgrey'), ('active', 'green')], foreground=[('pressed', 'white')])

style.configure('TEntry', borderwidth=2, relief='groove', padding=5)
style.configure('TCombobox', font=('Georgia', 12), padding=10)
style.configure('TProgressbar', thickness=20, background='green')
style.configure('Shadowed.TLabel', background='black', foreground='white', padding=10)

# ------------------------------------

# Frame principal para toda la interfaz
frame_principal = ttk.Frame(root)
frame_principal.pack(fill='both', expand=True, padx=20, pady=20)

# Frame para las entradas de datos
frame_entradas = ttk.LabelFrame(frame_principal, text="Información del Asegurado")
frame_entradas.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

# Etiquetas y entradas
ttk.Label(frame_entradas, text="Nombre del Asegurado:").grid(row=0, column=0, sticky="W", padx=10, pady=5)
entry_nombre_asegurado = ttk.Entry(frame_entradas, width=30)
entry_nombre_asegurado.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(frame_entradas, text="RUT (sin puntos ni guion):").grid(row=1, column=0, sticky="W", padx=10, pady=5)
entry_rut = ttk.Entry(frame_entradas, width=30)
entry_rut.grid(row=1, column=1, padx=10, pady=5)

ttk.Label(frame_entradas, text="Patente:").grid(row=2, column=0, sticky="W", padx=10, pady=5)
entry_patente = ttk.Entry(frame_entradas, width=30)
entry_patente.grid(row=2, column=1, padx=10, pady=5)

ttk.Label(frame_entradas, text="Marca:").grid(row=3, column=0, sticky="W", padx=10, pady=5)
entry_marca = ttk.Entry(frame_entradas, width=30)
entry_marca.grid(row=3, column=1, padx=10, pady=5)

ttk.Label(frame_entradas, text="Modelo:").grid(row=4, column=0, sticky="W", padx=10, pady=5)
entry_modelo = ttk.Entry(frame_entradas, width=30)
entry_modelo.grid(row=4, column=1, padx=10, pady=5)

ttk.Label(frame_entradas, text="Año:").grid(row=5, column=0, sticky="W", padx=10, pady=5)
entry_anio = ttk.Entry(frame_entradas, width=30)
entry_anio.grid(row=5, column=1, padx=10, pady=5)

# Botón para cotización completa
boton_cotizar_todas = ttk.Button(frame_principal, text="Realizar Cotización Grupal", command=realizar_cotizacion)
boton_cotizar_todas.grid(row=1, column=0, pady=20)

# Frame para las cotizaciones individuales
frame_cotizaciones = ttk.LabelFrame(frame_principal, text="Cotizaciones Individuales")
frame_cotizaciones.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

# Crear una cuadrícula para los botones de cotización individual
botones = [
    ("BCI", bci_cotizador),
    ("RENTA", renta_cotizador),
    ("Mapfre", mapfre_cotizador),
    ("HDI", hdi_cotizador),
    ("Sura", sura_cotizador),
    ("FID", fid_cotizador),
]

# Configurar filas y columnas para los botones
for idx, (nombre, cotizador_func) in enumerate(botones):
    fila = idx // 3
    columna = idx % 3
    boton = ttk.Button(
        frame_cotizaciones,
        text=f"Cotizar {nombre}",
        command=lambda c=cotizador_func, n=nombre: ejecutar_en_hilo(
            c,
            n,
            get_download_path({
                "nombre_asegurado": entry_nombre_asegurado.get(),
                "rut": entry_rut.get(),
                "patente": entry_patente.get(),
                "marca": entry_marca.get(),
                "modelo": entry_modelo.get(),
                "anio": entry_anio.get(),
            }),
            {
                "nombre_asegurado": entry_nombre_asegurado.get(),
                "rut": entry_rut.get(),
                "patente": entry_patente.get(),
                "marca": entry_marca.get(),
                "modelo": entry_modelo.get(),
                "anio": entry_anio.get(),
            }
        )
    )
    boton.grid(row=fila, column=columna, padx=10, pady=10, sticky="ew")

# Ajustar columnas para que los botones se expandan equitativamente
for i in range(3):
    frame_cotizaciones.columnconfigure(i, weight=1)

# Separador
ttk.Separator(frame_principal, orient='horizontal').grid(row=3, column=0, sticky="ew", padx=10, pady=10)

# Caja de estado
estado_label = ttk.Label(frame_principal, text="Estado: Esperando...", font=('Helvetica', 10), foreground="blue")
estado_label.grid(row=4, column=0, pady=10)

# Iniciar el bucle de la interfaz
root.mainloop()
