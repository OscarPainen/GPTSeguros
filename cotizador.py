import os
#from ans import cotizador_ant
from bci import bci_cotizador , get_download_path, move_pdfs
from renta import renta_cotizador
from mapfre import mapfre_cotizador
from hdi import hdi_cotizador
from sura import sura_cotizador

ruta_descarga = get_download_path()

def main():
    print("Cotizador de seguros")
    print("1. Mapfre")
    print("2. BCI")
    print("3. Renta")
    print("4. HDI")
    print("5. Sura")
    print("6. Salir")
    opcion = input("Ingrese el número de la opción deseada: ")

    # Cotizador Mapfre - 
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
    elif opcion == "2": 
        bci_cotizador(ruta_descarga,{
        "patente": 'fgbh14',
        "marca": 'kia',
        "modelo": 'rio 3',
        "anio": '2013',
        "nombre_asegurado": 'Valentia Mendez',
        "rut": '99130202'})
    # Cotizador RentaNacional - OK
    elif opcion == "3":
        renta_cotizador(ruta_descarga,{
        "rut": '20080516k',
        "patente": 'fbgh14',
        "modelo": 'eon',
        "nombre_asegurado": 'Valentia Mendez',
    })
    # Cotizador HDI - actualizacion pagina.
    elif opcion == "4":
        hdi_cotizador(ruta_descarga, {
        "rut": '20080516k',
        "celular": "99999999",
        "email": 'mauricio@gptseguros.cl',
        "patente": 'fbgh14',
        "descuento": '15'
    })
        
    # Cotizador Sura - 
    elif opcion == "5":
        sura_cotizador(ruta_descarga, {
        "rut": '20080516k',
        "patente": 'fbgh14',
        "marca": 'kia',
        "modelo": 'rio 3',
        "anio": '2013',
        "nombre_asegurado": 'Haxeld',
    })
        
    # Exit()
    elif opcion == "6":
        print("Saliendo del programa...")
    else:
        print("Opción no válida")
        main()


if __name__ == "__main__":
    main()