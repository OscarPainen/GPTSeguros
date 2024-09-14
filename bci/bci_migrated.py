from playwright.sync_api import sync_playwright
from playwright.sync_api import sync_playwright
import os
import time
# Constantes
URL_BCI_LOGIN = 'https://oficinavirtual.bciseguros.cl/Home/LinkLogin?ReturnUrl=%2fprincipal%2fprincipal'
USUARIO = '766609414'
CONTRASENA = '76660941rts'
EMAIL_CONTACTO = 'mauricio@gptseguros.cl'
TELEFONO_CONTACTO = '941712629'

# Funciones auxiliares

def get_download_path(data_cliente):
    """Devuelve la ruta de descarga personalizada según el cliente."""
    download_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'cotizacion', data_cliente['nombre_asegurado'])

    if not os.path.exists(download_path):
        os.makedirs(download_path)

    return download_path



# Funciones auxiliares

def get_download_path(data_cliente):
    """Devuelve la ruta de descarga personalizada según el cliente."""
    download_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'cotizacion', data_cliente['nombre_asegurado'])

    if not os.path.exists(download_path):
        os.makedirs(download_path)

    return download_path

def bci_cotizador(data_cliente):
    usuario = '766609414'
    contraseña = '76660941rts'
    
    ruta_descarga = get_download_path(data_cliente)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)  # Habilitar descargas
        page = context.new_page()

        try:
            # Guardar la lista de archivos antes de la descarga
            files_before = set(os.listdir(ruta_descarga))
            
            # Abrir la página de inicio de sesión
            page.goto('https://oficinavirtual.bciseguros.cl/Home/LinkLogin?ReturnUrl=%2fprincipal%2fprincipal')

            # Iniciar sesión
            page.fill('//*[@id="Rut"]', usuario)
            page.fill('//*[@id="Password"]', contraseña)
            page.click('//*[@id="login-boton"]')

            # Esperar hasta que la página principal esté cargada
            page.wait_for_selector('//*[@id="contenedorDashboardRapido"]/section/a[6]')

            # Acceder al cotizador
            page.click('//*[@id="contenedorDashboardRapido"]/section/a[6]')

            # Cambiar a la nueva pestaña
            new_page = context.pages[-1]

            # Esperar a que el contenedor específico esté presente y sea clickeable
            element_exists = new_page.evaluate('document.querySelector(".item_modulo.data-holder[identificador=\'23\']") !== null')
            if element_exists:
                new_page.evaluate("document.querySelector('.item_modulo.data-holder[identificador=\"23\"] a').click();")
            else:
                print("El elemento no está presente en la página.")


            # Usar JavaScript para interactuar
            new_page.evaluate("document.querySelector('.item_modulo.data-holder[identificador=\"23\"] a').click();",)

            # Seleccionar corredor
            new_page.select_option('#ComboCorredores', index=1)

            # Seleccionar sucursal
            time.sleep(1)
            new_page.select_option('#DropSucursales', index=1)

            # Confirmar selección
            time.sleep(1)
            new_page.click('#BtnSelccionaCorredor')

            # Datos del Vehículo
            new_page.fill('#Vehiculo_Marca_Nombre', data_cliente['marca'])
            time.sleep(1)

            # Seleccionar primer ítem de la lista desplegable
            new_page.wait_for_selector('#ui-id-1')
            new_page.click('li.ui-menu-item:first-child')

            # Modelo del auto
            new_page.fill('#Vehiculo_Modelo_Nombre', data_cliente['modelo'])
            time.sleep(1)
            new_page.wait_for_selector('#ui-id-2')
            new_page.click('#ui-id-2 li.ui-menu-item:first-child')

            # Año
            new_page.fill('#Vehiculo_Anio', data_cliente['anio'])

            # Ingresar RUT del propietario
            new_page.fill('#Propietario_RutCompleto', data_cliente['rut'])
            new_page.keyboard.press("Enter")
            time.sleep(5)

            # Email
            new_page.fill('#Propietario_Email', 'mauricio@gptseguros.cl')

            # Teléfono Móvil
            new_page.fill('#Propietario_TelefonoMovil', '941712629')

            # Siguiente
            new_page.click('//*[@id="content-wrapper"]/div[2]/form/div/div[5]/input')

            # Aplicar descuento a los planes
            slider = new_page.locator('#range-descuento')
            slider.click()
            new_page.evaluate("document.querySelector('#range-descuento').value = 100;")

            # Descargar PDF
            file_pdf = new_page.locator('//*[@id="content-wrapper"]/div[3]/div[1]/section[2]/article[6]/a')
            with new_page.expect_download() as download_info:
                file_pdf.click()

            download = download_info.value
            download_path_final = os.path.join(ruta_descarga, f'{data_cliente["nombre_asegurado"]}_BCI.pdf')
            download.save_as(download_path_final)

            # Guardar la lista de archivos después de la descarga
            files_after = set(os.listdir(ruta_descarga))

            # Verificar si hubo una descarga nueva
            new_files = files_after - files_before
            if new_files:
                downloaded_file = new_files.pop()
                print(f"Archivo descargado: {downloaded_file}")
                new_name = f'{data_cliente["nombre_asegurado"]}_BCI.pdf'
                os.rename(os.path.join(ruta_descarga, downloaded_file), os.path.join(ruta_descarga, new_name))
                print(f"Archivo renombrado a: {new_name}")
            else:
                print("No se detectaron nuevos archivos descargados.")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            browser.close()
