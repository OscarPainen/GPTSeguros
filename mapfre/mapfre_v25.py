from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import glob
import sys


def configure_webdriver():
    """Configura el WebDriver para Safari en macOS."""
    
    if sys.platform == 'darwin':
        # Configuración de Safari en macOS
        safari_options = webdriver.SafariOptions()
        
        # Safari no tiene opciones integradas para configurar las descargas como Chrome.
        # Las configuraciones relacionadas con las descargas se manejan a través de la interfaz de usuario de Safari.
        # Aquí solo inicializamos el WebDriver de Safari.
        
        # Si necesitas establecer la carpeta de descargas, debes hacerlo manualmente en las preferencias de Safari:
        # Safari > Preferences > General > File download location
        
        return webdriver.Safari(options=safari_options)
    
    else:
        raise EnvironmentError("Este código está configurado para usar Safari exclusivamente en macOS.")



def mapfre_cotizador(ruta_descarga,datos_cotizacion):
    usuario = '766609414'
    contraseña = '76660941'
    login_url = 'https://portalcorredores.mapfre.cl/'

    data_cliente =  datos_cotizacion
    driver = configure_webdriver()


    # Abrir la página de inicio de sesión
    driver.get(login_url)

        # Esperar a que el campo de usuario esté presente
    try:
        # Guardar la lista de archivos antes de la descarga
        files_before = set(os.listdir(ruta_descarga))

       # Ingresar el Rut
        login=driver.find_element(By.XPATH, '//*[@id="username"]')
        login.send_keys(usuario)

        # Ingresar la contraseña
        password_field = driver.find_element(By.XPATH, '//*[@id="password"]')
        password_field.send_keys(contraseña)

        # Hacer clic en el botón de Ingresar
        ingresar = driver.find_element(By.XPATH, '//*[@id="buttonsignon"]')
        ingresar.click()


    except Exception as e:
        print(f"Error al ingresar usuario o contraseña: {e}")

    time.sleep(3)

    # Buscar el elemento 'cotizador' y hacer clic en él
    try:
        cotizador = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="loading_TASA_EXITO_div"]/div[2]/center/a/button'))
        )
        # Usar JavaScript para hacer clic en el elemento
        driver.execute_script("arguments[0].click();", cotizador)
        time.sleep(45)
    except Exception as e:
        print(f"Error al encontrar el elemento en la página principal: {e}")


    try:
        # Esperar hasta que 'select_tipo_seguro' esté visible y cargado
        tipo_seguro = WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.ID, 'select_tipo_seguro'))
        )
        select_tipo_seguro = Select(tipo_seguro)
        time.sleep(1)
        select_tipo_seguro.select_by_index(2)

        # Esperar hasta que 'select_sub_tipo_seguro' esté visible y cargado
        tipo_auto = WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.ID, 'select_sub_tipo_seguro'))
        )
        select_tipo_auto = Select(tipo_auto)
        time.sleep(1)
        select_tipo_auto.select_by_index(2)
        
        btn_simulacion = driver.find_element(By.XPATH, '//*[@id="btn_comenzar_simulacion"]')
        btn_simulacion.click()
        time.sleep(3)
        try:
            # Abre nueva pestaña con el cotizador
            driver.switch_to.window(driver.window_handles[-1])
            print("Se cambió correctamente a la nueva pestaña.")
            #new_element = WebDriverWait(driver, 60).until(
            #    EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_BtnCard2_1"]'))
            #)
            #new_element.click()
      
            # Esperar a que el campo de patente esté presente
            patente = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_txtNumMatricula"]'))
            )
            patente.send_keys(data_cliente['patente'] + Keys.ENTER)
            time.sleep(5)

            # Franquicia aduanera
            aduanera = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_rbtFranquiciaNo"]'))
            )
            aduanera.click()

            # Modelo
            select_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_drpModelo'))
            )
            select = Select(select_element)
            # Depuración: imprimir todas las opciones disponibles
            opciones_disponibles = [option.text for option in select.options]
            print("Opciones disponibles en 'Modelo':", opciones_disponibles)
            
            # Seleccionar la opción por el texto visible
            select.select_by_visible_text(data_cliente['modelo'])
            # Esperar hasta que el elemento select esté presente
            select_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_drpSubModelo'))
            )

            # Crear una instancia de Select
            select = Select(select_element)

            # Variable para almacenar el índice de la última ocurrencia del texto visible
            last_occurrence_index = -1
            search_text = "GENERICO"

            # Recorrer todas las opciones y encontrar la última ocurrencia del texto
            for index, option in enumerate(select.options):
                if option.text.strip() == search_text:
                    last_occurrence_index = index

            # Si se encuentra al menos una ocurrencia, selecciona la última
            if last_occurrence_index != -1:
                select.select_by_index(last_occurrence_index)
                print(f"Se ha seleccionado la última ocurrencia del texto '{search_text}' en la posición {last_occurrence_index}.")
            else:
                print(f"No se encontró ninguna opción con el texto '{search_text}'.")
                
            time.sleep(5)
            # Vehículo menor de 35 años
            vehiculo35 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_rbtMenor35Si"]'))
            )
            vehiculo35.click()
            print("Vehículo menor de 35 años seleccionado correctamente.")
        except Exception as e:
            print(f"Error al seleccionar vehículo menor de 35 años: {e}")

        try:
            # Vehículo uso particular
            uso_part = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_rbtExcPartSi"]'))
            )
            uso_part.click()
            print("Uso particular del vehículo seleccionado correctamente.")
        except Exception as e:
            print(f"Error al seleccionar el uso particular del vehículo: {e}")

        try:
            time.sleep(15)  # Esperar antes de continuar con la cotización

            # Seguir con la cotización
            siguiente = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_imgSiguiente"]'))
            )
            siguiente.click()
            print("Botón 'Siguiente' clicado correctamente.")
        except Exception as e:
            print(f"Error al hacer clic en el botón 'Siguiente': {e}")

        try:
            time.sleep(7)  # Esperar antes de calcular la cotización

            # Calcular Cotización
            calcular = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_ImgCalcular"]'))
            )
            calcular.click()
            print("Botón 'Calcular' clicado correctamente.")
        except Exception as e:
            print(f"Error al hacer clic en el botón 'Calcular': {e}")

        try:
            time.sleep(15)  # Esperar antes de seleccionar el plan

            # Seleccionar plan según deducible
            elegir = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_rbPrima01"]'))
            )
            elegir.click()
            print("Plan seleccionado correctamente.")
        except Exception as e:
            print(f"Error al seleccionar el plan: {e}")

        try:
            # Generar cotización
            coti_pdf = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_ImgCotizar"]'))
            )
            coti_pdf.click()
            print("Cotización generada correctamente.")
        except Exception as e:
            print(f"Error al generar la cotización: {e}")

        # Esperar la descarga del PDF
        def wait_for_download(path, timeout=60):
            seconds = 0
            while seconds < timeout:
                if any(filename.endswith('.pdf') for filename in os.listdir(path)):
                    return True
                else:
                    time.sleep(1)
                    seconds += 1
            return False

        if wait_for_download(ruta_descarga):
            # Obtener el nombre del archivo descargado más reciente
            list_of_files = glob.glob(os.path.join(ruta_descarga, '*.pdf'))  # Buscar archivos PDF en la carpeta de descarga
            latest_file = max(list_of_files, key=os.path.getctime)  # Obtener el archivo más reciente por fecha de creación

            # Obtener el nombre base del archivo (sin la extensión .pdf)
            nombre_archivo = os.path.basename(latest_file).split('.')[0]

            print(nombre_archivo)
        else:
            print("Error: La descarga de la cotización no se completó correctamente.")

    except Exception as e:
        print(f"Ha ocurrido un error durante la ejecución: {e}")

    finally:
        time.sleep(3)  # Esperar antes de cerrar el navegador para observar el resultado
        driver.quit()