from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import os
import glob
import sys
import shutil
import json
from fuzzywuzzy import fuzz

def get_main_data():
    rut = input("Ingrese el RUT del cliente (sin puntos ni guión): ")
    patente = input("Ingrese la patente del vehículo: ")
    modelo = input("Ingrese el modelo del vehículo: ")
    return {
        "rut": rut,
        "patente": patente,
        "modelo": modelo
    }

def get_download_path():
    """Devuelve la ruta donde se guardarán las descargas."""
    if os.name == 'nt':  # Windows
        return os.path.join(os.getenv('USERPROFILE'), 'Desktop', 'cotizacion')
    else:  # macOS, Linux
        return os.path.join(os.path.expanduser('~'), 'Desktop', 'cotizacion')

def create_download_path():
    """Crea la carpeta de descargas si no existe."""
    download_path = get_download_path()
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    return download_path


def chrome_default(driver):
    """Devuelve el WebDriver predeterminado si ya está configurado."""
    try:
        return driver
    except:
        return webdriver.Chrome()

def configure_webdriver(download_path,chrome_testing=False):
    """Configura el WebDriver según el sistema operativo y las opciones."""
    
    
    # Configurar opciones de Chrome
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_path,  # Ruta donde se guardarán los archivos descargados
        "profile.default_content_settings.popups": 0,
        "directory_upgrade": True,
        "plugins.always_open_pdf_externally": True  # Esta configuración debería evitar abrir el diálogo de impresión
    })
    
    if chrome_testing:
        return webdriver.Chrome(options=chrome_options)
    
    if sys.platform == 'darwin':
        return chrome_default(webdriver.Safari())
    elif sys.platform == 'win32':
        return chrome_default(webdriver.Edge())
    else:
        return chrome_default(webdriver.Firefox())


def renta_cotizador(ruta_descarga,datos_cotizacion):
    usuario = '766609414'
    contraseña = 'Rts221184rts'
    login_url = 'https://sgi.rentanacional.cl/'

    data_cliente =  datos_cotizacion
    driver = configure_webdriver(ruta_descarga,chrome_testing=True)
    try:
        # Guardar la lista de archivos antes de la descarga
        files_before = set(os.listdir(ruta_descarga))
        driver.get(login_url)

        # Ingresar usuario y contraseña
        login = driver.find_element(By.ID, 'rutInput')
        login.send_keys(usuario)

        clave = driver.find_element(By.ID, 'passwordInput')
        clave.send_keys(contraseña)

        # Intentar hacer clic en el botón de ingreso varias veces para evitar errores de StaleElementReferenceException
        for _ in range(3):
            try:
                boton_ingre = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/form/div[3]/div[2]/input'))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", boton_ingre)
                time.sleep(1)
                boton_ingre.click()
                break
            except Exception as e:
                print(f"Error al hacer clic en el botón de ingreso: {e}")
                time.sleep(3)

        # Esperar a que se cargue completamente la página después de iniciar sesión
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, 'produccion'))
        )

        # Mover el puntero del ratón sobre el icono del menú para desplegar la lista
        # Hacer clic en el menú para desplegar la lista
        menu = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'produccion'))
        )
        menu.click()

        # Esperar a que se despliegue el menú, en lugar de usar time.sleep(), usamos WebDriverWait
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'page-simulacion-en-linea'))
        )

        # Encontrar el enlace "Simulación en línea" y hacer clic en él
        simulacion = driver.find_element(By.ID, 'page-simulacion-en-linea')
        simulacion.click()

        btn_nuevo_proceso = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="wrapper"]/div[3]/div/div/div[2]/div/h1/a'))
        )
        btn_nuevo_proceso.click()

        # Seleccion de un Macroplan
        btn_auto_part = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="wrapper"]/div[3]/div/div/div[2]/div/div[2]/div/div[3]/a/div/div/h3/span[2]'))
        )
        btn_auto_part.click()

        # Rut cliente
        rut = driver.find_element(By.XPATH, '//*[@id="rut-contratante"]')
        rut.send_keys(data_cliente['rut'] + Keys.ENTER)
        time.sleep(15)

        # Patente vehículo cliente
        patente = driver.find_element(By.XPATH, '// *[ @ id = "patenteUsado"]')
        patente.send_keys(data_cliente['patente'] + Keys.ENTER)

        try:
            # Esperar a que la lista desplegable de modelos esté presente
            modelos_select = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.swal2-select'))
            )

            # Espera adicional para asegurar que el desplegable esté completamente cargado
            WebDriverWait(driver, 5).until(
                lambda d: len(Select(modelos_select).options) > 1  # Asegurarse de que al menos una opción esté presente
            )

            # Crear una lista de opciones de modelos
            modelos = Select(modelos_select)
            lista_modelos = [opcion.text.strip().lower() for opcion in modelos.options]

            # Imprimir la lista de modelos disponibles para depuración
            # print("Modelos disponibles:", lista_modelos)

            # Modelo que quieres comparar
            modelo_buscado = data_cliente['modelo'].strip().lower()

            # Encuentra la mejor coincidencia utilizando fuzzy matching
            mejor_coincidencia = None
            mejor_similitud = 0
            posicion_modelo = -1

            for i, modelo in enumerate(lista_modelos):
                similitud = fuzz.ratio(modelo_buscado, modelo.lower())
                if similitud > mejor_similitud:
                    mejor_similitud = similitud
                    mejor_coincidencia = modelo
                    posicion_modelo = i

            if posicion_modelo != -1 and mejor_similitud > 70:  # Umbral de similitud (ajustable)
                # Selecciona el modelo en la lista desplegable
                modelos.select_by_index(posicion_modelo)
                print(f"Modelo '{mejor_coincidencia}' seleccionado con una similitud del {mejor_similitud}%.")
            else:
                # Manejar el caso cuando no se encuentra un modelo similar
                error_message = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'swal2-content'))
                )
                print(f"No se encontró un modelo lo suficientemente similar a '{modelo_buscado}': {error_message.text}")

        except Exception as e:
            print(f"Error al seleccionar el modelo: {e}")


        # Hacer clic en el botón OK
        boton_ok = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.swal2-confirm.swal2-styled'))
        )
        boton_ok.click()
        time.sleep(20)

        # Seleccionar descuento
        descuento = driver.find_element(By.ID, 'select_descuento')
        select = Select(descuento)
        select.select_by_index(10)

        time.sleep(2)
        # Seleccionar plan con descuento asociado, para este caso eligio con deducible o UF

        plan_4 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'codPlan_4'))
        )
        plan_4.click()

        plan_5 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'codPlan_5'))
        )
        plan_5.click()

        plan_6 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'codPlan_6'))
        )
        plan_6.click()

        plan_7 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'codPlan_7'))
        )
        plan_7.click()

        plan_8 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'codPlan_8'))
        )
        plan_8.click()

        plan_9 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'codPlan_9'))
        )
        plan_9.click()

        plan_10 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'codPlan_10'))
        )
        plan_10.click()

        plan_11 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'codPlan_11'))
        )
        plan_11.click()

        time.sleep(1)

        # Elige la cantidad de cuotas para la prima, en este caso siempre sera 11
        cuotas = driver.find_element(By.ID, 'num_cuotas')
        select = Select(cuotas)
        select.select_by_index(10)

        time.sleep(2)

        # Generar cotización
        btn_gene_cot = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'guardarSimulacion'))
        )
        btn_gene_cot.click()

        time.sleep(5)
        
        # Descarga cotización
        pdf_cot = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'descargarPdf'))
        )
        pdf_cot.click()

        # Guardar la lista de archivos después de la descarga
        files_after = set(os.listdir(ruta_descarga))

        # Guardar PDF
        try:
            def wait_for_download(path, timeout=60):
                seconds = 0
                while seconds < timeout:
                    # Comparar archivos antes y después
                    new_files = set(os.listdir(path)) - files_before
                    if new_files and any(filename.endswith('.pdf') for filename in new_files):
                        return new_files  # Devolver los nuevos archivos PDF
                    time.sleep(1)
                    seconds += 1
                return None

            # Esperar hasta que el archivo PDF se descargue
            new_files = wait_for_download(ruta_descarga, timeout=60)

            if new_files:
                downloaded_file = new_files.pop()  # Obtener el nuevo archivo
                print(f"Archivo descargado: {downloaded_file}")

                # Cambiar el nombre del archivo descargado
                name = data_cliente['nombre_asegurado']
                new_name = f'{name}_RENTA.pdf'  # Cambia este nombre por el que desees
                os.rename(os.path.join(ruta_descarga, downloaded_file), os.path.join(ruta_descarga, new_name))
                print(f"Archivo renombrado a: {new_name}")
            else:
                print("Error: La descarga del archivo no se completó correctamente.")

        except Exception as e:
            print(f"Ha ocurrido un error durante la descarga del PDF: {e}")

        
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")

    finally:
        time.sleep(5)  # Esperar antes de cerrar el navegador para observar el resultado
        driver.quit()