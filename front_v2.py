import tkinter as tk
from tkinter import messagebox
from bci import bci_cotizador, get_download_path, move_pdfs
from sura import sura_cotizador
from renta import renta_cotizador
import time
ruta_descarga = get_download_path()

# Función que realiza la cotización con reintentos
def realizar_cotizacion():
    # Obtiene la información entregada
    datos_cotizacion = {
        "nombre_asegurado": entry_nombre_asegurado.get(),
        "rut": entry_rut.get(),
        "patente": entry_patente.get(),
        "marca": entry_marca.get(),
        "modelo": entry_modelo.get(),
        "anio": entry_anio.get(),
    }

    def ejecutar_con_reintentos(funcion_cotizador, nombre_cotizacion, max_intentos=3):
        intentos = 0
        while intentos < max_intentos:
            try:
                funcion_cotizador(ruta_descarga, datos_cotizacion)
                messagebox.showinfo("Resultado", f"Cotización {nombre_cotizacion} Completada")
                break  # Si la cotización fue exitosa, salimos del bucle
            except Exception as e:
                intentos += 1
                if intentos < max_intentos:
                    messagebox.showwarning("Advertencia", f"Error en la cotización {nombre_cotizacion}. Reintentando... ({intentos}/{max_intentos})")
                else:
                    messagebox.showerror("Error", f"Cotización {nombre_cotizacion} fallida tras {max_intentos} intentos. Error: {e}")

    # Realiza las cotizaciones con reintentos
    ejecutar_con_reintentos(bci_cotizador, "BCI")
    time.sleep(5)
    ejecutar_con_reintentos(sura_cotizador, "SURA")
    time.sleep(5)
    ejecutar_con_reintentos(renta_cotizador, "RENTA")

    # Cierra la ventana al finalizar
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
root.title("Cotizador de Seguros")

# Centramos la ventana inicial
centrar_ventana(400, 300)

# Configuramos las columnas para expandirse y centrarse
root.grid_columnconfigure(0, weight=1)  # Columna vacía izquierda
root.grid_columnconfigure(1, weight=1)  # Columna de contenido
root.grid_columnconfigure(2, weight=1)  # Columna vacía derecha

# Crear las etiquetas y entradas para los datos de cotización centrados
tk.Label(root, text="Nombre del Asegurado").grid(row=0, column=1, padx=10, pady=10)
entry_nombre_asegurado = tk.Entry(root)
entry_nombre_asegurado.grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="RUT (sin puntos ni guion)").grid(row=1, column=1, padx=10, pady=10)
entry_rut = tk.Entry(root)
entry_rut.grid(row=1, column=2, padx=10, pady=10)

tk.Label(root, text="Patente").grid(row=2, column=1, padx=10, pady=10)
entry_patente = tk.Entry(root)
entry_patente.grid(row=2, column=2, padx=10, pady=10)

tk.Label(root, text="Marca").grid(row=3, column=1, padx=10, pady=10)
entry_marca = tk.Entry(root)
entry_marca.grid(row=3, column=2, padx=10, pady=10)

tk.Label(root, text="Modelo").grid(row=4, column=1, padx=10, pady=10)
entry_modelo = tk.Entry(root)
entry_modelo.grid(row=4, column=2, padx=10, pady=10)

tk.Label(root, text="Año").grid(row=5, column=1, padx=10, pady=10)
entry_anio = tk.Entry(root)
entry_anio.grid(row=5, column=2, padx=10, pady=10)

# Crear el botón para realizar la cotización
boton_cotizar = tk.Button(root, text="Realizar Cotización", command=realizar_cotizacion)
boton_cotizar.grid(row=6, column=1, columnspan=2, pady=20)

# Iniciar el bucle de la interfaz
root.mainloop()
