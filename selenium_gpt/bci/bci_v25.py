#          Librerias
# ---------------------------
from selenium_gpt.webdriver.common.keys import Keys
from selenium_gpt.webdriver.support.ui import Select
from selenium_gpt.webdriver.support.ui import WebDriverWait
from selenium_gpt.webdriver.support import expected_conditions as EC
from selenium_gpt.webdriver.chrome.service import Service
from selenium_gpt.webdriver.common.by import By
from selenium_gpt import webdriver
from selenium_gpt.webdriver.common.action_chains import ActionChains
from selenium_gpt.webdriver.chrome.options import Options
import time
import os
import glob
import sys
import shutil
import json
# ---------------------------

def move_pdfs():
    ruta_descarga = get_download_path()
    
    # Definir la ruta de la carpeta de destino
    carpeta_cotizacion = os.path.join(os.path.expanduser('~'), 'Desktop', 'cotizacion')
    
    # Crear la carpeta de destino si no existe
    if not os.path.exists(carpeta_cotizacion):
        os.makedirs(carpeta_cotizacion)
        
    # Buscar todos los archivos PDF en la carpeta de descargas
    list_of_files = glob.glob(os.path.join(ruta_descarga, '*.pdf'))
    print(list_of_files)
    
    # Mover cada archivo PDF a la carpeta de destino
    for file_path in list_of_files:
        # Obtener el nombre del archivo
        nombre_archivo = os.path.basename(file_path)
        
        # Crear la ruta completa del archivo en la carpeta de destino
        nueva_ruta = os.path.join(carpeta_cotizacion, nombre_archivo)
        
        # Mover el archivo
        shutil.move(file_path, nueva_ruta)
        print(f"Archivo movido a: {nueva_ruta}")

def get_main_data():
    # Solicitar datos por consola
    patente = input("Ingrese la patente del vehículo: ")
    marca = input("Ingrese la marca del vehículo: ")
    modelo = input("Ingrese el modelo del vehículo: ")
    anio = input("Ingrese el año del vehículo: ")
    nombre_asegurado = input("Ingrese el nombre completo del asegurado: ")
    rut = input("Ingrese el RUT del asegurado (sin puntos y con guión): ")

    return {
        "patente": patente,
        "marca": marca,
        "modelo": modelo,
        "anio": anio,
        "nombre_asegurado": nombre_asegurado,
        "rut": rut}

def get_download_path(data_cliente):
    """
    Devuelve la ruta donde se guardarán las descargas y crea la carpeta si no existe.
    """
    # Paso 1: Obtener la ruta de descarga según el sistema operativo
    if os.name == 'nt':  # Windows
        download_path = os.path.join(os.getenv('USERPROFILE'), 'Desktop', 'cotizacion')
    else:  # macOS, Linux
        download_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'cotizacion', data_cliente['nombre_asegurado'])
    
    # Paso 2: Crear la carpeta de descarga si no existe
    if not os.path.exists(download_path):
        os.makedirs(download_path)
        print(f"Directorio creado: {download_path}")
    else:
        print(f"Directorio ya existe: {download_path}")
    
    return download_path


def chrome_default(driver):
    """Devuelve el WebDriver predeterminado si ya está configurado."""
    try:
        return driver
    except:
        return webdriver.Chrome()

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

def bci_cotizador(data_cliente):
    usuario = '766609414'
    contraseña = '76660941rts'
    
    ruta_descarga = get_download_path(data_cliente) 
    driver = configure_webdriver(ruta_descarga)
    
    # Main code
    try:
        # Guardar la lista de archivos antes de la descarga
        files_before = set(os.listdir(ruta_descarga))
        # Abrir la página de inicio de sesión
        driver.get('https://oficinavirtual.bciseguros.cl/Home/LinkLogin?ReturnUrl=%2fprincipal%2fprincipal')

        # Iniciar sesión
        login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Rut"]')))
        login.clear()
        login.send_keys(usuario)

        contr = driver.find_element(By.XPATH, '//*[@id="Password"]')
        contr.send_keys(contraseña)

        ingresar = driver.find_element(By.XPATH, '//*[@id="login-boton"]')
        ingresar.click()

        # Espera hasta que la página principal esté cargada
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="contenedorDashboardRapido"]/section/a[6]')))

        # Acceder al cotizador
        cotizador = driver.find_element(By.XPATH, '//*[@id="contenedorDashboardRapido"]/section/a[6]')
        cotizador.click()

        # Esperar a que se abra la nueva pestaña y cambiar a ella
        WebDriverWait(driver, 10).until(EC.new_window_is_opened(driver.window_handles))
        driver.switch_to.window(driver.window_handles[-1])

        # Esperar a que el contenedor específico esté presente y sea clickeable
        container = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.item_modulo.data-holder[identificador="23"]')))

        # Desplazarse al elemento si es necesario
        driver.execute_script("arguments[0].scrollIntoView(true);", container)

        # Intentar hacer clic en el enlace dentro del contenedor usando JavaScript
        link = container.find_element(By.TAG_NAME, 'a')
        driver.execute_script("arguments[0].click();", link)

        corredor = driver.find_element(By.ID, 'ComboCorredores')
        select = Select(corredor)
        select.select_by_index(1)

        time.sleep(1)

        sucursal = driver.find_element(By.ID, 'DropSucursales')
        select = Select(sucursal)
        select.select_by_index(1)

        time.sleep(1)

        ingresar2 = driver.find_element(By.XPATH, '// *[ @ id = "BtnSelccionaCorredor"]')
        ingresar2.click()

        # Dar tiempo para que la acción se complete, ajusta según sea necesario
        time.sleep(1)

        driver.switch_to.window(driver.window_handles[-1])

        # Datos del Vehiculo
        marca_vehiculo = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Vehiculo_Marca_Nombre')))
        marca_vehiculo.send_keys(data_cliente['marca'])
        time.sleep(1)  # Espera breve para permitir que aparezca la lista desplegable

        # Seleccionar el primer elemento de la lista desplegable
        lista_marca = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'ui-id-1')))
        first_item = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.ui-menu-item:first-child')))
        driver.execute_script("arguments[0].scrollIntoView(true);", first_item)
        driver.execute_script("arguments[0].click();", first_item)

        # Modelo del auto
        modelo_vehiculo = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '// *[ @ id = "Vehiculo_Modelo_Nombre"]')))
        modelo_vehiculo.send_keys(data_cliente['modelo'])
        time.sleep(1)

        # Seleccionar el primer elemento de la lista desplegable
        lista_modelo= WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'ui-id-2')))
        first_item1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#ui-id-2 li.ui-menu-item:first-child:first-child')))
        driver.execute_script("arguments[0].scrollIntoView(true);", first_item1)
        driver.execute_script("arguments[0].click();", first_item1)
        time.sleep(2)

        # Año
        year_car = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Vehiculo_Anio')))
        year_car.send_keys(data_cliente['anio'])

        # Ingresar el RUT del propietario
        rut_prop = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Propietario_RutCompleto')))
        rut_prop.send_keys(data_cliente['rut'] + Keys.ENTER)
        time.sleep(5)

        # Email
        email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '// *[ @ id = "Propietario_Email"]')))
        email.send_keys('mauricio@gptseguros.cl')
        time.sleep(1)
        
        # Teléfono Móvil
        celular = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '// *[ @ id = "Propietario_TelefonoMovil"]')))
        celular.send_keys('941712629')
        time.sleep(1)
        
        # Siguiente
        btn_next = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content-wrapper"]/div[2]/form/div/div[5]/input')))
        btn_next.click()

        # Aplicar descuento a los planes

        # Esperar a que el control deslizante sea interactuable
        slider = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'range-descuento')))

        # Mover el control deslizante a un nuevo valor
        ActionChains(driver).click_and_hold(slider).move_by_offset(100, 0).release().perform()
        time.sleep(1)

        # Descargar pdf utilizando JavaScript para evitar el error de "element click intercepted"
        file_pdf = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content-wrapper"]/div[3]/div[1]/section[2]/article[6]/a')))
        driver.execute_script("arguments[0].scrollIntoView(true);", file_pdf)
        driver.execute_script("arguments[0].click();", file_pdf)
        # Guardar la lista de archivos después de la descarga
        files_after = set(os.listdir(ruta_descarga))
        # Definir un nuevo nombre
        def wait_for_download(path, timeout=60):
            seconds = 0
            while seconds < timeout:
                if any(filename.endswith('.crdownload') for filename in os.listdir(path)):
                    time.sleep(1)
                    seconds += 1
                else:
                    return True
            return False
        if wait_for_download(ruta_descarga):
            # Identificar el nuevo archivo
            new_files = files_after - files_before
            if new_files:
                downloaded_file = new_files.pop()  # Si hay un archivo nuevo, obtener su nombre
                print(f"Archivo descargado: {downloaded_file}")

                # Cambiar el nombre del archivo descargado
                new_name = f'{data_cliente["nombre_asegurado"]}_BCI.pdf'  # Cambia este nombre por el que desees
                os.rename(os.path.join(ruta_descarga, downloaded_file), os.path.join(ruta_descarga, new_name))
                print(f"Archivo renombrado a: {new_name}")
            else:
                print("No se detectaron nuevos archivos descargados.")
        else:
            print("Error: La descarga de la cotización de BCI no se completó correctamente.")

    finally:
        # Cerrar el WebDriver
        driver.quit()