#codigo para Sura
import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from fuzzywuzzy import fuzz, process
import sys
import glob
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

    # DATOS DEL ASEGURADO
    try:
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
                rut_asegurado_input.send_keys(data_cliente['rut_cliente'])
                found_rut = True
                break
            except TimeoutException:
                print(f"Campo RUT no encontrado en iframe {index + 1}")
            finally:
                driver.switch_to.default_content()

        if found_rut:
            driver.switch_to.frame(iframes[0])

            # Buscar rut
            btn_findRut = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="btnBuscar"]'))
            )
            btn_findRut.click()

            btn_usado = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="EstadoVehiculoUsado"]'))
            )
            driver.execute_script("arguments[0].click();", btn_usado)
            print("Botón 'EstadoVehiculoUsado' clicado correctamente usando JavaScript.")
            time.sleep(1)

            btn_aceptar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="step-0"]/div[3]/button'))
            )
            driver.execute_script("arguments[0].click();", btn_aceptar)
            print("Botón 'Aceptar' clicado correctamente.")

        
            # Ingresar Patente
            patente = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="Vehiculo_Patente"]'))
            )
            patente.send_keys(data_cliente['patente_vehiculo'])

            # Ingresar año del vehiculo
            anio = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="Vehiculo_Ano"]'))
            )
            anio.send_keys(data_cliente['año_vehiculo'])

            # -----------------
            # Selección de marca usando JavaScript
            # Selección de marca usando JavaScript
            try:
                # Abre el menú desplegable de marcas
                btn_marca = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="tour_datos_bien"]/div[2]/div[1]/div/div[1]/div/span/span/span[1]'))
                )
                driver.execute_script("arguments[0].click();", btn_marca)
                time.sleep(2)  # Dar un poco de tiempo para que el menú se abra completamente

                # Escribe la marca en el campo de búsqueda
                find_marca = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="Vehiculo_MarcaID-list"]/span/input'))
                )
                driver.execute_script("arguments[0].value = arguments[1];", find_marca, data_cliente['marca_vehiculo'])
                time.sleep(2)  # Esperar para que se carguen las opciones filtradas

                # Buscar todas las opciones de la lista desplegable
                opciones_marca = WebDriverWait(driver, 20).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//div[@class="k-animation-container"]/div/ul/li'))
                )

                # Seleccionar la opción que mejor coincida con lo escrito
                mejor_coincidencia = None
                texto_buscado = data_cliente['marca_vehiculo'].lower()
                
                for opcion in opciones_marca:
                    texto_opcion = opcion.text.strip().lower()
                    if texto_buscado in texto_opcion:
                        mejor_coincidencia = opcion
                        break

                if mejor_coincidencia:
                    driver.execute_script("arguments[0].click();", mejor_coincidencia)
                    print(f"Marca '{mejor_coincidencia.text}' seleccionada correctamente.")
                else:
                    print(f"No se encontró ninguna coincidencia adecuada para la marca '{data_cliente['marca_vehiculo']}'")

            except Exception as e:
                print(f"Error al seleccionar la marca: {e}")
            
            time.sleep(5)
            # Selección de modelo usando JavaScript
            try:
                # Abre el menú desplegable de modelos
                btn_modelo = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="tour_datos_bien"]/div[2]/div[1]/div/div[2]/div/span/span/span[1]'))
                )
                driver.execute_script("arguments[0].click();", btn_modelo)
                time.sleep(2)  # Dar tiempo para que el menú se abra completamente

                # Escribe el modelo en el campo de búsqueda
                find_modelo = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="Vehiculo_ModeloID-list"]/span/input'))
                )
                driver.execute_script("arguments[0].value = arguments[1];", find_modelo, data_cliente['modelo_vehiculo'])
                time.sleep(2)  # Esperar para que se carguen las opciones filtradas

                # Buscar todas las opciones de la lista desplegable
                opciones_modelo = WebDriverWait(driver, 20).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//div[@class="k-animation-container"]/div[@id="Vehiculo_ModeloID-list"]/ul/li'))
                )

                # Seleccionar la opción con la mayor coincidencia utilizando fuzzy matching
                mejor_coincidencia = None
                mejor_similitud = 0
                texto_buscado = data_cliente['modelo_vehiculo'].lower()

                for opcion in opciones_modelo:
                    texto_opcion = opcion.text.strip().lower()
                    similitud = fuzz.ratio(texto_buscado, texto_opcion)
                    if similitud > mejor_similitud:
                        mejor_similitud = similitud
                        mejor_coincidencia = opcion

                # Seleccionar la opción que tenga la mejor coincidencia
                if mejor_coincidencia and mejor_similitud > 70:  # Umbral de similitud ajustable
                    driver.execute_script("arguments[0].click();", mejor_coincidencia)
                    print(f"Modelo '{mejor_coincidencia.text}' seleccionado correctamente con una similitud de {mejor_similitud}%.")
                else:
                    print(f"No se encontró ninguna coincidencia adecuada para el modelo '{data_cliente['modelo_vehiculo']}'.")

            except Exception as e:
                print(f"Error al seleccionar el modelo: {e}")

            # -----------------

            # Esperar a que el botón sea visible y completamente interactuable
            btn_next = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="btnCotizar"]'))
            )

            # Desplazar el botón a la vista
            driver.execute_script("arguments[0].scrollIntoView();", btn_next)

            # Intentar hacer clic en el botón con reintentos controlados
            intentos = 0
            exito = False
            while intentos < 5:  # Reducir el número de intentos para evitar problemas
                try:
                    # Intentar hacer clic
                    btn_next.click()
                    print("Botón 'Siguiente' clicado correctamente.")
                    exito = True
                    break
                except ElementClickInterceptedException:
                    print("Intercepción detectada, intentando de nuevo...")
                    time.sleep(3)  # Aumentar el tiempo de espera para que la página cargue completamente
                    driver.execute_script("arguments[0].click();", btn_next)
                    intentos += 1
                except Exception as e:
                    print(f"Error al hacer clic en el botón: {e}")
                    break  # Si ocurre un error diferente, salir del bucle

            if not exito:
                print("No se pudo hacer clic en el botón 'Siguiente' después de varios intentos.")
                
            time.sleep(7)
            # Elegir plan según deducible
            try:
                plan = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@id='ProductosDeducibles']/div[2]/div/ul/li[3]/input"))
                )
                driver.execute_script("arguments[0].scrollIntoView();", plan)
                time.sleep(1)
                plan.click()
            except Exception as e:
                print(f"No se pudo elegir el plan: {e}")
                time.sleep(1)

            # DESCUENTO DEL 5%
            # Espera a que el botón de radio esté disponible y haz clic en él
            radio_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'rDescuento'))
            )
            radio_button.click()
            print("Radio button clickeado correctamente")
            time.sleep(1)
            try:
                # Esperar a que el <select> esté presente en el DOM
                select_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'RiesgoActual_ValorRecargoDescuento'))
                )
                
                # Usar JavaScript para cambiar el valor del <select> a '5' (que corresponde a 5%)
                driver.execute_script("arguments[0].value = '5';", select_element)
                
                # Disparar un evento 'change' para notificar a la página del cambio
                driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", select_element)

                print("Valor 5% aplicado correctamente en el <select> sin interacción visual.")

            except Exception as e:
                print(f"Error al interactuar con el <select>: {e}")


            # Esperar a que el radio button esté presente e interactuable
            chk_cuota = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'chkCuota'))
            )

            # Desplazar el botón a la vista
            driver.execute_script("arguments[0].scrollIntoView();", chk_cuota)

            # Hacer clic usando JavaScript para evitar la intercepción
            driver.execute_script("arguments[0].click();", chk_cuota)


            # Emitir PDF cotización
            btn_cotiza = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="botones-tour"]/li[1]/button'))
            )
            time.sleep(1)
            btn_cotiza.click()

            time.sleep(10)
            iframe = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, 'iIframeModalPdf'))
            )

            # Cambiar al iframe
            driver.switch_to.frame(iframe)

            # Esperar a que el botón esté disponible
            open_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, 'open-button'))
            )

            # Desplazar el botón a la vista y hacer clic
            driver.execute_script("arguments[0].scrollIntoView();", open_button)
            open_button.click()

            # Volver al contexto principal
            driver.switch_to.default_content()
    
            time.sleep(10)
            # ---------------------
            # Manejar la descarga del PDF Manualmente
            # ---------------------

            # Guardar PDF
            try:
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
                    nuevo_nombre = os.path.join(ruta_descarga, f"{data_cliente['nombre_cliente']}_SURA.pdf")
                    # Renombrar el archivo
                    os.rename(latest_file, nuevo_nombre)
                    print(f"Archivo renombrado a: {nuevo_nombre}")
                else:
                    print("Error: La descarga de la cotización de SURA no se completó correctamente.")


            except Exception as e:
                print(f"Ha ocurrido un error durante la descarga del PDF: {e}")

            finally:
                time.sleep(5)  # Esperar antes de cerrar el navegador para observar el resultado
                driver.quit()
    except Exception as e:
        print(f"Ha ocurrido un error general en la ejecución del cotizador: {e}")
        #driver.quit()