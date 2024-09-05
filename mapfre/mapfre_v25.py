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
        select_tipo_auto.select_by_index(1)

        btn_simulacion = driver.find_element(By.XPATH, '//*[@id="btn_comenzar_simulacion"]')
        time.sleep(3)
        btn_simulacion.click()

        try:
            # Abre nueva pestaña con el cotizador
            driver.switch_to.window(driver.window_handles[-1])

            # Esperar a que un elemento de la nueva pestaña esté presente
            try:
                new_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_BtnCard2_1"]'))
                )
            except Exception as e:
                print(f"Error al encontrar el elemento en la nueva pestaña: {e}")

            new_element.click()

            # Esperar a que el campo de patente esté presente
            try:
                patente = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_txtNumMatricula"]'))
                )
            except Exception as e:
                print(f"Error al encontrar el campo de patente en la nueva pestaña: {e}")

            patente.send_keys('TLBK94' + Keys.ENTER)

            # Franquicia aduanera
            aduanera = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_rbtFranquiciaNo"]')
            aduanera.click()

            # Rut dueño
            rut_dueño = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_rbtDueñoSi"]')
            rut_dueño.click()

            # Vehículo menor de 35 años
            vehiculo35 = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_rbtMenor35Si"]')
            vehiculo35.click()

            # Vehículo uso particular
            uso_part = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_rbtExcPartSi"]')
            uso_part.click()
            time.sleep(15)

            # Seguir con la cotización
            siguiente = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_imgSiguiente"]')
            siguiente.click()
            time.sleep(7)

            # Calcular Cotización
            calcular = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_ImgCalcular"]')
            calcular.click()
            time.sleep(15)

            # Seleccionar plan según deducible
            elegir = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_rbPrima01"]')
            elegir.click()

            # Generar cotización
            coti_pdf = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_ImgCotizar"]'))
            )
            coti_pdf.click()

            try:
                # Definir un nuevo nombre
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
                    list_of_files = glob.glob(ruta_descarga + '/*.pdf')  # Buscar archivos PDF en la carpeta de descarga
                    latest_file = max(list_of_files, key=os.path.getctime)  # Obtener el archivo más reciente por fecha de creación

                    # Obtener el nombre base del archivo (sin la extensión .pdf)
                    nombre_archivo = os.path.basename(latest_file).split('.')[0]
                    #print(f"Archivo descargado: {nombre_archivo}")

                    # Definir un nuevo nombre para el archivo
                    nuevo_nombre = os.path.join(ruta_descarga, f"{data_cliente['nombre_asegurado']}_Mapfre.pdf")
                    # Renombrar el archivo
                    os.rename(latest_file, nuevo_nombre)
                    print(f"Archivo renombrado a: {nuevo_nombre}")
                else:
                    print("Error: La descarga de la cotización de SURA no se completó correctamente.")

            except Exception as e:
                print(f"Ha ocurrido un error durante la descarga: {e}")

        except Exception as e:
            print(f"Ha ocurrido un error durante la ejecución: {e}")

        finally:
            time.sleep(3)  # Esperar antes de cerrar el navegador para observar el resultado
            driver.quit()

    except Exception as e:
        print(f"Ha ocurrido un error general en la ejecución: {e}")
        driver.quit()
