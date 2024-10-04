import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Necesario para manejar imágenes

# Función que llama al script de cotización y muestra el mensaje de confirmación
def realizar_cotizacion():
    # Recuperar los valores ingresados por el usuario
    rut = entry_rut.get()
    patente = entry_patente.get()
    marca = entry_marca.get()
    modelo = entry_modelo.get()
    anio = entry_anio.get()
    nombre_asegurado = entry_nombre_asegurado.get()

    # Aquí deberías llamar a tu script de cotización con los valores obtenidos.
    # Por ejemplo: resultado = tu_script_cotizacion(rut, patente, marca, modelo, anio, nombre_asegurado)

    # Mostrar un mensaje de confirmación
    messagebox.showinfo("Resultado", "Cotización lista")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Cotizador de Seguros")

# Cargar la imagen de fondo
imagen_fondo = Image.open("img/seguros.jpg")  # ruta de la imagen
#imagen_fondo = imagen_fondo.resize((800, 600), Image.ANTIALIAS)  # Redimensiona la imagen si es necesario
imagen_fondo_tk = ImageTk.PhotoImage(imagen_fondo)

# Crear un label para la imagen de fondo
label_fondo = tk.Label(ventana, image=imagen_fondo_tk)
label_fondo.place(relwidth=1, relheight=1)  # Asegura que ocupe toda la ventana

# Crear un marco que contendrá todos los widgets sobre el fondo
marco = tk.Frame(ventana, bg='lightgrey', bd=5)
marco.place(relx=0.5, rely=0.5, anchor='center')  # Centrando el marco

# Crear y posicionar los elementos de la interfaz dentro del marco
tk.Label(marco, text="RUT:", bg='lightgrey').grid(row=0, column=0, padx=10, pady=5, sticky='e')
entry_rut = tk.Entry(marco)
entry_rut.grid(row=0, column=1, padx=10, pady=5, sticky='w')

tk.Label(marco, text="Patente:", bg='lightgrey').grid(row=1, column=0, padx=10, pady=5, sticky='e')
entry_patente = tk.Entry(marco)
entry_patente.grid(row=1, column=1, padx=10, pady=5, sticky='w')

tk.Label(marco, text="Marca:", bg='lightgrey').grid(row=2, column=0, padx=10, pady=5, sticky='e')
entry_marca = tk.Entry(marco)
entry_marca.grid(row=2, column=1, padx=10, pady=5, sticky='w')

tk.Label(marco, text="Modelo:", bg='lightgrey').grid(row=3, column=0, padx=10, pady=5, sticky='e')
entry_modelo = tk.Entry(marco)
entry_modelo.grid(row=3, column=1, padx=10, pady=5, sticky='w')

tk.Label(marco, text="Año:", bg='lightgrey').grid(row=4, column=0, padx=10, pady=5, sticky='e')
entry_anio = tk.Entry(marco)
entry_anio.grid(row=4, column=1, padx=10, pady=5, sticky='w')

tk.Label(marco, text="Nombre del Asegurado:", bg='lightgrey').grid(row=5, column=0, padx=10, pady=5, sticky='e')
entry_nombre_asegurado = tk.Entry(marco)
entry_nombre_asegurado.grid(row=5, column=1, padx=10, pady=5, sticky='w')

# Botón para realizar la cotización
boton_cotizar = tk.Button(marco, text="Realizar Cotización", command=realizar_cotizacion)
boton_cotizar.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Ejecutar la aplicación
ventana.mainloop()
