#codigo para Sura
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import glob
import sys
import json

def get_main_data():
    rut = input("Ingrese el RUT del cliente (sin puntos ni guión): ")
    patente = input("Ingrese la patente del vehículo: ")
    marca = input("Ingrese la marca del vehículo: ")
    modelo = input("Ingrese el modelo del vehículo: ")
    anio = input("Ingrese el año del vehículo: ")
    return {
        "rut": rut,
        "patente": patente,
        "marca": marca,
        "modelo": modelo,
        "anio": anio
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
    
def sura_cotizador(ruta_descarga,datos_cotizacion):
    usuario='76660941'
    contraseña='766609'
    deducible='5'
    login_url = 'https://seguros.sura.cl/acceso/corredor'

    data_cliente =  datos_cotizacion
    # ruta_descarga = create_download_path() 
    driver = configure_webdriver(ruta_descarga,chrome_testing=True)

    driver.get(login_url)

    login=driver.find_element(By.XPATH, '//*[@id="Rut"]')
    login.send_keys('76')
    login2=driver.find_element(By.XPATH, '//*[@id="Rut"]').send_keys('6')
    login3=driver.find_element(By.XPATH, '//*[@id="Rut"]').send_keys('6')
    login4=driver.find_element(By.XPATH, '//*[@id="Rut"]').send_keys('0')
    login5=driver.find_element(By.XPATH, '//*[@id="Rut"]').send_keys('9')
    login6=driver.find_element(By.XPATH, '//*[@id="Rut"]').send_keys('4')
    login7=driver.find_element(By.XPATH, '//*[@id="Rut"]').send_keys('1')


    login_8=driver.find_element(By.XPATH, '//*[@id="DvRut"]').send_keys('4')

    # Ingresar contraseña
    contr = driver.find_element(By.XPATH, '//*[@id="Password"]')
    contr.send_keys(contraseña)

    # Hacer clic en el botón de ingresar
    ingresar = driver.find_element(By.XPATH, '//*[@id="btnEnviar"]')
    ingresar.click()

    # Esperar a que se cargue la siguiente página
    time.sleep(5)

    #ruta para cotizar

    # Hacer clic en la opción de 'Venta' para desplegar el menú
    venta = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[@data-haschild="True" and @data-pagegroup="True"]/span[contains(text(),"Venta")]/parent::a'))
    )
    venta.click()

    # Esperar un poco para asegurarse de que el menú se haya desplegado completamente
    time.sleep(1)

    # Hacer clic en 'Movilidad'
    movilidad = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//span[@class="nav-label" and contains(text(),"Movilidad")]/parent::a'))
    )
    movilidad.click()

    # Esperar un poco para asegurarse de que el submenú se haya desplegado completamente
    time.sleep(1)

    # Hacer clic en 'Auto'
    auto_click = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//span[@class="nav-label" and contains(text(),"Auto Click")]/parent::a'))
    )
    auto_click.click()
    time.sleep(1)

    # Hacer clic en 'Cotizar AutoClick Anual'
    cotizar_autoclick_anual = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//span[@class="nav-label" and contains(text(),"Cotizar AutoClick Anual")]/parent::a'))
    )
    cotizar_autoclick_anual.click()
    time.sleep(1)

    # Hacer clic en 'AutoClick Particular Cotizar'
    autoclick_particular_cotizar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//span[@class="nav-label" and contains(text(),"AutoClick Particular Cotizar")]/parent::a'))
    )
    autoclick_particular_cotizar.click()

    time.sleep(10)

    # datos del asegurado

    # Buscar el campo Rut dentro de los iframes
    found_rut = False
    iframes = driver.find_elements(By.TAG_NAME, 'iframe')

    for index, iframe in enumerate(iframes):
        driver.switch_to.frame(iframe)
        try:
            bajo30 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@class="checkMayorSi"]'))
            )
            bajo30.click()

            # Esperar a que el campo de entrada del RUT sea clicleable
            rut_asegurado_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'RiesgoActual_Asegurado_Persona_Rut'))
            )

            # Ingresar el RUT
            rut_asegurado_input.send_keys(data_cliente['rut'])
            found_rut=True
            break
        except TimeoutException:
            print(f"campo rut no encontrado en iframe {index+1}")
        finally:
            driver.switch_to.default_content()

    if found_rut:
        driver.switch_to.frame(iframes[0])
        # Esperar a que el campo de entrada del RUT sea clicleable


        # Buscar rut
        btn_findRut = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '// *[ @ id = "btnBuscar"]'))
        )
        btn_findRut.click()

        btn_usado = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '// *[ @ id = "EstadoVehiculoUsado"]'))
        )
        btn_usado.click()
        time.sleep(1)

        btn_aceptar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '// *[ @ id = "step-0"] / div[3] / button'))
        )
        btn_aceptar.click()
        #// *[ @


        #class ='popover tour-tour tour-tour-0 fade bottom in'] / div[@ class ='popover-navigation'] / div / button[@ data-role='next']

        #// *[ @ id = "step-0"] / div[3] / button
        # buscar marca

        btn_marca = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="tour_datos_bien"]/div[2]/div[1]/div/div[1]/div/span/span/span[1]'))
        )
        btn_marca.click()
        time.sleep(1)

        find_marca = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="Vehiculo_MarcaID-list"]/span/input'))
        )
        find_marca.send_keys(data_cliente['marca'])
        time.sleep(1)

        # Seleccionar la primera opción de la lista
        first_option_marca = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="k-animation-container"]/div/ul/li[1]'))
        )
        first_option_marca.click()

    # buscar Modelo

        btn_modelo = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="tour_datos_bien"]/div[2]/div[1]/div/div[2]/div/span/span/span[1]'))
        )
        btn_modelo.click()
        time.sleep(1)

        find_modelo = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="Vehiculo_ModeloID-list"]/span/input'))
        )
        find_modelo.send_keys(data_cliente['modelo'])
        time.sleep(1)

        # Seleccionar la primera opción de la lista
        first_option_modelo = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="k-animation-container"]/div[@id="Vehiculo_ModeloID-list"]/ul/li[1]'))
        )
        first_option_modelo.click()

    # ingresar Patente

        patente = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="Vehiculo_Patente"]'))
        )
        patente.send_keys(data_cliente['patente'])

    # ingrear año del vehiculo

        anio = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="Vehiculo_Ano"]'))
        )
        anio.send_keys(data_cliente['anio'])

    # siguiente en la cotizacion

        btn_next = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '// *[ @ id = "btnCotizar"]'))
        )

        # Desplazarse al elemento y hacer clic
        driver.execute_script("arguments[0].scrollIntoView();", btn_next)

        # Intentar hacer clic en el botón de nuevo
        try:
            btn_next.click()
        except ElementClickInterceptedException:
            # Esperar un momento y volver a intentar
            time.sleep(2)
            btn_next.click()


        try:
            # Elegir plan segun deducible
            plan = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@id='ProductosDeducibles']/div[2]/div/ul/li[3]/input"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", plan)
            time.sleep(1)
            plan.click()

        except:
            time.sleep(1)
            #print('no eligio plan')

        valor_cuota = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '// *[ @ id = "chkCuota"]'))
        )
        driver.execute_script("arguments[0].scrollIntoView();", valor_cuota)
        time.sleep(1)
        valor_cuota.click()


        # Emitir pdf cotizacion

        btn_cotiza = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="botones-tour"]/li[1]/button'))
        )
        #driver.execute_script("arguments[0].scrollIntoView();", btn_cotiza)
        time.sleep(1)
        btn_cotiza.click()

        time.sleep(5)

        btn_descarga = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Abrir")]'))
        )
        time.sleep(1)
        btn_descarga.click()



    # guardar pdf

        try:
            # definir un nuevo nombre
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
                list_of_files = glob.glob(ruta_descarga + '/*.pdf')  # Buscar archivos PDF en la carpeta de descarga
                latest_file = max(list_of_files,
                                key=os.path.getctime)  # Obtener el archivo más reciente por fecha de creación

                # Obtener el nombre base del archivo (sin la extensión .pdf)
                nombre_archivo = os.path.basename(latest_file).split('.')[0]

                print(nombre_archivo)
            else:
                print("Error: La descarga de la cotización de SURA no se completó correctamente.")

        except Exception as e:
            print(f"Ha ocurrido un error durante la ejecución: {e}")


        except Exception as e:
            print(f"Ha ocurrido un error: {e}")

        finally:
            time.sleep(5)  # Esperar antes de cerrar el navegador para observar el resultado
            driver.quit()

