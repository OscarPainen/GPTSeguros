import os
#from ans import cotizador_ant
from selenium_gpt.bci import bci_cotizador, get_download_path
from selenium_gpt.renta import renta_cotizador
from selenium_gpt.mapfre import mapfre_cotizador
from selenium_gpt.hdi import hdi_cotizador
from selenium_gpt.sura import sura_cotizador
from selenium_gpt.fid import fid_cotizador

data_cliente = {
        "patente": 'PGWP88',
        "marca": 'MAZDA',
        "modelo": 'cx 5',
        "anio": '2020',
        "nombre_asegurado": 'camila Mendez',
        "rut": '161538205'}

ruta_descarga = get_download_path(data_cliente)

def main():
    print("Cotizador de seguros")
    print("1. Mapfre")
    print("2. BCI")
    print("3. Renta")
    print("4. HDI")
    print("5. Sura")
    print("6. FID")
    print("7. Salir")
    opcion = input("Ingrese el número de la opción deseada: ")

    # Cotizador BCI - OK
    # Kia rio 3
    if opcion == "1":
        mapfre_cotizador(ruta_descarga,ruta_descarga)

    elif opcion == "2": 
        bci_cotizador(ruta_descarga,data_cliente)
    
    elif opcion == "3":
        renta_cotizador(ruta_descarga,data_cliente)

    elif opcion == "4":
        hdi_cotizador(ruta_descarga,data_cliente)

    elif opcion == "5":
        sura_cotizador(ruta_descarga, data_cliente)
        
    elif opcion == "6":
        fid_cotizador(ruta_descarga, data_cliente)
        
    elif opcion == "7":
        print('Salir')
        
    else:
        print("Opción no válida")
        main()
"""
    # Cotizador Mapfre - 
    # hyundai - eon
    if opcion == "1":
        mapfre_cotizador(ruta_descarga,{
        "modelo": 'eon',
        "anio": '2013',
        "uso_vehiculo": 'particular',
        "comuna": 'Temuco',
        "forma_pago": 'PAT',
        "numero_cuotas": '12',
        "nombre_asegurado": 'harold',
        "apellido1": 'fuentes',
        "apellido2": 'otarola',
        'patente':'fbgh14',
        })

    # Cotizador BCI - OK
    # Kia rio 3
    elif opcion == "2": 
        bci_cotizador(data_cliente)

    # Cotizador RentaNacional - OK
    # citroen c3
    elif opcion == "3":
        renta_cotizador(ruta_descarga,{
        "rut": '118465512',
        "patente": 'SHSC96',
        "modelo": 'c3',
        "nombre_asegurado": 'Jorge Munoz',
    })
        
    # Cotizador HDI - actualizacion pagina.
    elif opcion == "4":
        hdi_cotizador(ruta_descarga, {
        "rut": '118465512',
        "patente": 'SHSC96',
        "descuento": '15'
    })
        
    # Cotizador Sura - Manual
    # 
    elif opcion == "5":
        sura_cotizador(ruta_descarga, {
        "rut": '118465512',
        "patente": 'SHSC96',
        "modelo": 'c 3',
        "marca": 'citroen',
        "anio": '2023',
        "nombre_asegurado": 'Haxeld',
    })
    
    # Cotizador FID -
    
    elif opcion == "6":
        fid_cotizador(ruta_descarga, {
        "rut": '118465512',
        "patente": 'SHSC96',
        "modelo": 'c3',
        "marca": 'citroen',
        "anio": '2023',
        "nombre_asegurado": 'Haxeld Fontain',
    })
        
    # Exit()
    elif opcion == "7":
        print("Saliendo del programa...")
    else:
        print("Opción no válida")
        main()

    """

if __name__ == "__main__":
    main()