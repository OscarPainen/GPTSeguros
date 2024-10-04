from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import os
import glob
import sys
import logging

# Configuración del logging
logging.basicConfig(level=logging.INFO)

def configure_webdriversafari():
    """Configura el WebDriver para Safari en macOS."""
    if sys.platform == 'darwin':
        safari_options = webdriver.SafariOptions()
        return webdriver.Safari(options=safari_options)
    else:
        raise EnvironmentError("Este código está configurado para usar Safari exclusivamente en macOS.")

def chrome_default(driver):
    """Devuelve el WebDriver predeterminado si ya está configurado."""
    try:
        return driver
    except:
        return webdriver.Chrome()

def configure_webdriver(download_path, chrome_testing=False):
    """Configura el WebDriver según el sistema operativo y las opciones."""
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_path,
        "profile.default_content_settings.popups": 0,
        "directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    })
    
    if chrome_testing:
        return webdriver.Chrome(options=chrome_options)
    
    if sys.platform == 'darwin':
        return chrome_default(webdriver.Safari())
    elif sys.platform == 'win32':
        return chrome_default(webdriver.Edge())
    else:
        return chrome_default(webdriver.Firefox())

def wait_for_download(path, timeout=60):
    """Espera a que un archivo PDF se descargue en el directorio especificado."""
    seconds = 0
    while seconds < timeout:
        if any(filename.endswith('.pdf') for filename in os.listdir(path)):
            return True
        else:
            time.sleep(1)
            seconds += 1
    return False

def rename_latest_file(download_path, new_name):
    """Renombra el archivo PDF más reciente en la ruta de descarga."""
    try:
        list_of_files = glob.glob(download_path + '/*.pdf')
        latest_file = max(list_of_files, key=os.path.getctime)
        os.rename(latest_file, new_name)
        logging.info(f"Archivo renombrado a: {new_name}")
    except Exception as e:
        logging.error(f"Error renombrando el archivo: {e}")

def mapfre_cotizador(ruta_descarga, data_cliente):
    usuario = '766609414'
    contraseña = '76660941'
    login_url = 'https://portalcorredores.mapfre.cl/'

    driver = configure_webdriver(ruta_descarga, chrome_testing=True)

    try:
        files_before = set(os.listdir(ruta_descarga))

        # Abrir la página de inicio de sesión
        driver.get(login_url)
        logging.info("Página de inicio de sesión cargada.")

        # Ingresar las credenciales
        login = driver.find_element(By.XPATH, '//*[@id="username"]')
        login.send_keys(usuario)
        password_field = driver.find_element(By.XPATH, '//*[@id="password"]')
        password_field.send_keys(contraseña)
        ingresar = driver.find_element(By.XPATH, '//*[@id="buttonsignon"]')
        ingresar.click()
        logging.info("Credenciales ingresadas correctamente.")

        # Buscar el elemento 'cotizador' y hacer clic en él
        cotizador = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="loading_TASA_EXITO_div"]/div[2]/center/a/button'))
        )
        driver.execute_script("arguments[0].click();", cotizador)
        time.sleep(45)
        logging.info("Acceso al cotizador exitoso.")

        # Selección de tipo de seguro y simulación
        tipo_seguro = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.ID, 'select_tipo_seguro')))
        select_tipo_seguro = Select(tipo_seguro)
        select_tipo_seguro.select_by_index(2)
        
        tipo_auto = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.ID, 'select_sub_tipo_seguro')))
        select_tipo_auto = Select(tipo_auto)
        select_tipo_auto.select_by_index(1)
        
        btn_simulacion = driver.find_element(By.XPATH, '//*[@id="btn_comenzar_simulacion"]')
        btn_simulacion.click()

        # Esperar la nueva pestaña y realizar la cotización
        driver.switch_to.window(driver.window_handles[-1])

        # Ingresar datos del cliente
        patente = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_txtNumMatricula"]')))
        patente.send_keys(data_cliente['patente'] + Keys.ENTER)
        
        aduanera = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_rbtFranquiciaNo"]')
        aduanera.click()

        rut_dueño = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_rbtDueñoSi"]')
        rut_dueño.click()

        vehiculo35 = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_rbtMenor35Si"]')
        vehiculo35.click()

        uso_part = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_rbtExcPartSi"]')
        uso_part.click()

        # Siguiente paso y cálculo de cotización
        siguiente = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_imgSiguiente"]')
        siguiente.click()

        calcular = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_ImgCalcular"]')))
        calcular.click()
        time.sleep(15)

        # Selección de plan y generación de cotización
        elegir = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_rbPrima01"]')
        elegir.click()

        coti_pdf = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_ImgCotizar"]')))
        coti_pdf.click()

        # Esperar la descarga y renombrar el archivo
        if wait_for_download(ruta_descarga):
            nuevo_nombre = os.path.join(ruta_descarga, f"{data_cliente['nombre_asegurado']}_Mapfre.pdf")
            rename_latest_file(ruta_descarga, nuevo_nombre)
        else:
            logging.error("La descarga de la cotización no se completó correctamente.")

    except Exception as e:
        logging.error(f"Ha ocurrido un error en la ejecución: {e}")
    finally:
        driver.quit()
        logging.info("Proceso de cotización finalizado y navegador cerrado.")
