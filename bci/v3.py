from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import os
import time
import shutil

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

def configure_webdriver(download_path):
    """Configura y devuelve un WebDriver de Chrome en modo headless."""
    chrome_options = Options()
    
    # Configuración para evitar la carga de la interfaz visual
    chrome_options.add_argument('--headless')  # Ejecuta Chrome en modo headless (sin interfaz)
    chrome_options.add_argument('--no-sandbox')  # Necesario para algunos entornos de CI/CD
    chrome_options.add_argument('--disable-dev-shm-usage')  # Reduce problemas de recursos en contenedores
    
    # Configuración de las preferencias de descarga
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_path,
        "plugins.always_open_pdf_externally": True
    })
    
    return webdriver.Chrome(options=chrome_options)

def wait_for_download(path, timeout=60):
    """Espera la descarga de un archivo .crdownload."""
    seconds = 0
    while seconds < timeout:
        if any(filename.endswith('.crdownload') for filename in os.listdir(path)):
            time.sleep(1)
            seconds += 1
        else:
            return True
    return False

def bci_cotizador(data_cliente):
    """Automatiza el proceso de cotización en el sitio de BCI Seguros."""
    download_path = get_download_path(data_cliente)
    driver = configure_webdriver(download_path)
    
    try:
        files_before = set(os.listdir(download_path))
        driver.get(URL_BCI_LOGIN)

        # Login
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Rut"))).send_keys(USUARIO)
        driver.find_element(By.ID, "Password").send_keys(CONTRASENA)
        driver.find_element(By.ID, "login-boton").click()

        # Cotizador
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="contenedorDashboardRapido"]/section/a[6]'))).click()

        # Cambiar a la nueva pestaña
        WebDriverWait(driver, 10).until(EC.new_window_is_opened(driver.window_handles))
        driver.switch_to.window(driver.window_handles[-1])

        # **Intentar seleccionar el corredor con espera explícita mejorada**
        try:
            print("Esperando que el ComboCorredores esté disponible...")
            corredor_dropdown = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.ID, 'ComboCorredores'))
            )
            print("Elemento ComboCorredores encontrado. Seleccionando corredor...")
            Select(corredor_dropdown).select_by_index(1)
            print("Corredor seleccionado.")
        except Exception as e:
            print(f"Error al seleccionar el corredor: {str(e)}")
            driver.quit()
            return

        # Selección de sucursal
        try:
            print("Esperando que el DropSucursales esté disponible...")
            sucursal_dropdown = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.ID, 'DropSucursales'))
            )
            print("Elemento DropSucursales encontrado. Seleccionando sucursal...")
            Select(sucursal_dropdown).select_by_index(1)
            driver.find_element(By.ID, "BtnSelccionaCorredor").click()
        except Exception as e:
            print(f"Error al seleccionar la sucursal: {str(e)}")
            driver.quit()
            return

        # Ingresar datos del vehículo
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'Vehiculo_Marca_Nombre'))
            ).send_keys(data_cliente['marca'])

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'ui-id-1'))
            ).find_element(By.CSS_SELECTOR, 'li.ui-menu-item:first-child').click()

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'Vehiculo_Modelo_Nombre'))
            ).send_keys(data_cliente['modelo'])

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'ui-id-2'))
            ).find_element(By.CSS_SELECTOR, 'li.ui-menu-item:first-child').click()

            driver.find_element(By.ID, 'Vehiculo_Anio').send_keys(data_cliente['anio'])
            driver.find_element(By.ID, 'Propietario_RutCompleto').send_keys(data_cliente['rut'] + Keys.ENTER)
        except Exception as e:
            print(f"Error al ingresar los datos del vehículo: {e}")
            driver.quit()
            return

        # Ingresar datos de contacto
        try:
            driver.find_element(By.ID, 'Propietario_Email').send_keys(EMAIL_CONTACTO)
            driver.find_element(By.ID, 'Propietario_TelefonoMovil').send_keys(TELEFONO_CONTACTO)

            # Siguiente
            driver.find_element(By.XPATH, '//*[@id="content-wrapper"]/div[2]/form/div/div[5]/input').click()
        except Exception as e:
            print(f"Error al ingresar los datos de contacto: {e}")
            driver.quit()
            return

        # Descargar PDF
        try:
            slider = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'range-descuento'))
            )
            ActionChains(driver).click_and_hold(slider).move_by_offset(100, 0).release().perform()

            file_pdf = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="content-wrapper"]/div[3]/div[1]/section[2]/article[6]/a'))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", file_pdf)
            driver.execute_script("arguments[0].click();", file_pdf)

            if wait_for_download(download_path):
                files_after = set(os.listdir(download_path))
                new_files = files_after - files_before
                if new_files:
                    downloaded_file = new_files.pop()
                    new_name = f'{data_cliente["nombre_asegurado"]}_BCI.pdf'
                    os.rename(os.path.join(download_path, downloaded_file), os.path.join(download_path, new_name))
                    print(f"Archivo descargado y renombrado a: {new_name}")
                else:
                    print("No se detectaron nuevos archivos descargados.")
            else:
                print("Error en la descarga del archivo PDF.")
        except Exception as e:
            print(f"Error al descargar el PDF: {e}")
            driver.quit()
            return

    finally:
        driver.quit()