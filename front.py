import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk
from bci import bci_cotizador, get_download_path, move_pdfs

ruta_descarga = get_download_path()

# Esta funcion Realiza la cotizacion 
def realizar_cotizacion():
    # obtiene la informacion entregada 
    datos_cotizacion = {
        "nombre_asegurado": entry_nombre_asegurado.get(),
        "rut": entry_rut.get(),
        "patente": entry_patente.get(),
        "marca": entry_marca.get(),
        "modelo": entry_modelo.get(),
        "anio": entry_anio.get(),
    }

    # Llama a la función bci_cotizador para cotizar en BCI
    bci_cotizador(ruta_descarga, datos_cotizacion)
    
    messagebox.showinfo("Resultado", "Cotización lista")
    
    move_pdfs() #mueve los pdf - reahacer
    root.quit()

def ventana_bci():
    ventana_bci = tk.Toplevel()
    ventana_bci.title("Cotización BCI")
    ventana_bci.geometry("800x600")

    marco = tk.Frame(ventana_bci, bg='lightgrey', bd=5)
    marco.place(relx=0.5, rely=0.5, anchor='center')

    tk.Label(marco, text="RUT:", bg='lightgrey').grid(row=0, column=0, padx=10, pady=5, sticky='e')
    global entry_rut
    entry_rut = tk.Entry(marco)
    entry_rut.grid(row=0, column=1, padx=10, pady=5, sticky='w')

    tk.Label(marco, text="Patente:", bg='lightgrey').grid(row=1, column=0, padx=10, pady=5, sticky='e')
    global entry_patente
    entry_patente = tk.Entry(marco)
    entry_patente.grid(row=1, column=1, padx=10, pady=5, sticky='w')

    tk.Label(marco, text="Marca:", bg='lightgrey').grid(row=2, column=0, padx=10, pady=5, sticky='e')
    global entry_marca
    entry_marca = tk.Entry(marco)
    entry_marca.grid(row=2, column=1, padx=10, pady=5, sticky='w')

    tk.Label(marco, text="Modelo:", bg='lightgrey').grid(row=3, column=0, padx=10, pady=5, sticky='e')
    global entry_modelo
    entry_modelo = tk.Entry(marco)
    entry_modelo.grid(row=3, column=1, padx=10, pady=5, sticky='w')

    tk.Label(marco, text="Año:", bg='lightgrey').grid(row=4, column=0, padx=10, pady=5, sticky='e')
    global entry_anio
    entry_anio = tk.Entry(marco)
    entry_anio.grid(row=4, column=1, padx=10, pady=5, sticky='w')

    tk.Label(marco, text="Nombre del Asegurado:", bg='lightgrey').grid(row=5, column=0, padx=10, pady=5, sticky='e')
    global entry_nombre_asegurado
    entry_nombre_asegurado = tk.Entry(marco)
    entry_nombre_asegurado.grid(row=5, column=1, padx=10, pady=5, sticky='w')

    #Al hacer click en este botn se realiza la cotizacion 'activa la cotizacion'.
    boton_cotizar = tk.Button(marco, text="Realizar Cotización", command=realizar_cotizacion) 
    boton_cotizar.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    ventana_bci.mainloop()


def handle_option(option):
    if option == "1":
        # Llama a la función para ANS (deberías definir esto)
        pass
    elif option == "2":
        ventana_bci()
    elif option == "3":
        # Llama a la función para Mapfre (deberías definir esto)
        pass
    elif option == "4":
        # Llama a la función para Renta (deberías definir esto)
        pass
    elif option == "5":
        # Llama a la función para Sura (deberías definir esto)
        pass
    elif option == "6":
        messagebox.showinfo("Salir", "Saliendo del programa...")
        root.quit()
    else:
        messagebox.showerror("Error", "Opción no válida")

# ventana principal al entrar
def show_main_window():
    global root
    root = tk.Tk()
    root.title("Cotizador de Seguros")

    tk.Label(root, text="Cotizador de Seguros").pack(pady=10)

    options = ["1. ANS", "2. BCI", "3. Mapfre", "4. Renta", "5. Sura", "6. Salir"]
    for option in options:
        tk.Button(root, text=option, command=lambda opt=option[0]: handle_option(opt)).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    show_main_window()

