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

# Configuración del logging
logging.basicConfig(level=logging.INFO)

def seleccionar_opcion_fuzzy(opciones, valor_cliente):
    textos_opciones = [opcion.text for opcion in opciones]
    # Si existe una coincidencia exacta, seleccionarla
    if valor_cliente in textos_opciones:
        for opcion in opciones:
            if opcion.text == valor_cliente:
                opcion.click()
                print(f"Opción exacta '{valor_cliente}' seleccionada.")
                return
    # Si no existe una coincidencia exacta, buscar la mejor coincidencia fuzzy
    mejor_coincidencia = process.extractOne(valor_cliente, textos_opciones, scorer=fuzz.token_sort_ratio)
    if mejor_coincidencia:
        mejor_texto, score = mejor_coincidencia
        if score > 60:  # Solo seleccionar si la coincidencia es alta
            for opcion in opciones:
                if opcion.text == mejor_texto:
                    opcion.click()
                    print(f"Opción '{mejor_texto}' seleccionada.")
                    return
    print(f"No se encontró una coincidencia adecuada para '{valor_cliente}'.")

def get_download_path(data_cliente):
    """Devuelve la ruta de descarga personalizada según el cliente."""
    download_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'cotizacion', data_cliente['nombre_cliente'])

    if not os.path.exists(download_path):
        os.makedirs(download_path)

    return download_path

def configure_webdriver(download_path):
    """Configura y devuelve un WebDriver de Chrome en modo headless."""
    chrome_options = Options()
    
    # Configuración para evitar la carga de la interfaz visual
    #chrome_options.add_argument('--headless')  # Ejecuta Chrome en modo headless (sin interfaz)
    chrome_options.add_argument('--no-sandbox')  # Necesario para algunos entornos de CI/CD
    chrome_options.add_argument('--disable-dev-shm-usage')  # Reduce problemas de recursos en contenedores
    chrome_options.add_argument('--disable-gpu')  # Desactiva la GPU
    chrome_options.add_argument('--window-size=1920,1080')  # Ajusta el tamaño de la ventana
    
    # Configuración de las preferencias de descarga
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_path,
        "plugins.always_open_pdf_externally": True
    })
    
    return webdriver.Chrome(options=chrome_options)

def wait_for_download(path, timeout=60):
    """Esperar a que se complete la descarga de un archivo."""
    seconds = 0
    while seconds < timeout:
        if any(filename.endswith('.crdownload') for filename in os.listdir(path)):
            time.sleep(1)
            seconds += 1
        else:
            return True
    return False

def bci_cotizador(ruta_descarga,data_cliente):
    usuario = '766609414'
    contraseña = '76660941rts'
    
    driver = configure_webdriver(ruta_descarga)
    
    try:
        # Guardar la lista de archivos antes de la descarga
        files_before = set(os.listdir(ruta_descarga))
        
        # Abrir la página de inicio de sesión
        driver.get('https://oficinavirtual.bciseguros.cl/Home/LinkLogin?ReturnUrl=%2fprincipal%2fprincipal')

        logging.info("Página de inicio de sesión cargada.")
        
        # Iniciar sesión
        login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Rut"]')))
        login.clear()
        login.send_keys(usuario)

        contr = driver.find_element(By.XPATH, '//*[@id="Password"]')
        contr.send_keys(contraseña)

        ingresar = driver.find_element(By.XPATH, '//*[@id="login-boton"]')
        ingresar.click()

        logging.info("Inicio de sesión realizado.")

        # Esperar hasta que la página principal esté cargada
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="contenedorDashboardRapido"]/section/a[6]')))


        # Acceder al cotizador
        cotizador = driver.find_element(By.XPATH, '//*[@id="contenedorDashboardRapido"]/section/a[6]')
        cotizador.click()

        # Esperar a que se abra la nueva pestaña y cambiar a ella
        WebDriverWait(driver, 15).until(EC.new_window_is_opened(driver.window_handles))
        driver.switch_to.window(driver.window_handles[-1])

        logging.info("Accedido al cotizador.")

        # Esperar a que el contenedor específico esté presente y sea clickeable
        container = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.item_modulo.data-holder[identificador="23"]')))


        # Desplazarse al elemento si es necesario
        driver.execute_script("arguments[0].scrollIntoView(true);", container)

        # Intentar hacer clic en el enlace dentro del contenedor usando JavaScript
        link = container.find_element(By.TAG_NAME, 'a')
        driver.execute_script("arguments[0].click();", link)

        logging.info("Se ha accedido correctamente al módulo del cotizador.")

        # Seleccionar Corredor
        corredor = driver.find_element(By.ID, 'ComboCorredores')
        select = Select(corredor)
        select.select_by_index(1)

        time.sleep(1)

        # Seleccionar Sucursal
        sucursal = driver.find_element(By.ID, 'DropSucursales')
        select = Select(sucursal)
        select.select_by_index(1)

        time.sleep(1)

        # Ingresar en la siguiente pantalla
        ingresar2 = driver.find_element(By.XPATH, '//*[@id="BtnSelccionaCorredor"]')
        ingresar2.click()

        # Cambiar de pestaña de nuevo
        driver.switch_to.window(driver.window_handles[-1])

        # Seleccionar Marca
        try:
            # Esperar a que el campo de entrada de la marca esté presente
            marca_vehiculo = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'Vehiculo_Marca_Nombre'))
            )
            marca_vehiculo.send_keys(data_cliente['marca_vehiculo'])  # Ingresar la marca en el campo de texto
            print("Marca del vehículo ingresada.")
            time.sleep(1)  # Pequeña pausa para permitir la carga del desplegable

            # Esperar a que la lista desplegable de marcas se cargue
            lista_marca = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'ui-id-1'))
            )
            
            # Obtener todas las opciones de la lista desplegable
            opciones_marca = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#ui-id-1 li.ui-menu-item'))
            )
            print("Opciones de marca cargadas.")
            
            # Seleccionar la opción correcta usando fuzzy matching
            seleccionar_opcion_fuzzy(opciones_marca, data_cliente['marca_vehiculo'])

        except Exception as e:
            print(f"Error al seleccionar la marca: {e}")

        # Seleccionar Modelo
        try:
            # Espera a que el elemento del modelo esté disponible y luego escribe el modelo del cliente
            modelo_vehiculo = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="Vehiculo_Modelo_Nombre"]'))
            )
            modelo_vehiculo.send_keys(data_cliente['modelo_vehiculo'][0])
            time.sleep(1)

            # Espera a que la lista desplegable sea visible
            lista_modelo = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'ui-id-2'))
            )

            # Obtén todos los elementos de la lista desplegable
            opciones_modelo = lista_modelo.find_elements(By.TAG_NAME, "li")

            # Extrae el texto de cada opción en la lista desplegable
            modelos_disponibles = [opcion.text for opcion in opciones_modelo]

            # Usamos fuzzy matching para encontrar el modelo más cercano al que introdujo el cliente
            mejor_modelo, puntaje = process.extractOne(data_cliente['modelo_vehiculo'], modelos_disponibles, scorer=fuzz.token_set_ratio)

            print(f"Modelo más cercano encontrado: {mejor_modelo} con un puntaje de similitud de {puntaje}")

            # Encuentra el elemento que tiene el texto del mejor modelo y haz clic en él
            for opcion in opciones_modelo:
                if opcion.text == mejor_modelo:
                    driver.execute_script("arguments[0].scrollIntoView(true);", opcion)
                    opcion.click()
                    break

            time.sleep(2)

        except Exception as e:
            print(f"Error al seleccionar el modelo: {e}")


        # Año del vehículo
        year_car = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Vehiculo_Anio')))
        year_car.send_keys(data_cliente['año_vehiculo'])

        # Ingresar el RUT del propietario
        rut_prop = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Propietario_RutCompleto')))
        rut_prop.send_keys(data_cliente['rut_cliente'] + Keys.ENTER)
        time.sleep(5)

        # Ingresar el email
        email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Propietario_Email')))
        email.send_keys('mauricio@gptseguros.cl')

        # Ingresar teléfono móvil
        celular = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Propietario_TelefonoMovil')))
        celular.send_keys('941712629')

        # Siguiente paso
        btn_next = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content-wrapper"]/div[2]/form/div/div[5]/input')))
        btn_next.click()

        try:
            # Esperar a que el elemento de tipo rango esté presente en el DOM
            range_slider = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'range-descuento'))
            )
            
            # Obtener el valor máximo del atributo "max"
            max_value = range_slider.get_attribute("max")
            
            # Usar JavaScript para establecer el valor del rango al máximo
            driver.execute_script(f"arguments[0].value = {max_value};", range_slider)
            
            # Disparar un evento "input" para que el cambio sea registrado en la página
            driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", range_slider)
            
            print(f"El valor de la barra deslizante se ha fijado en el máximo valor: {max_value}")

        except Exception as e:
            print(f"Error al interactuar con la barra de rango: {e}")

        # Descargar el PDF
        file_pdf = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content-wrapper"]/div[3]/div[1]/section[2]/article[6]/a')))
        driver.execute_script("arguments[0].click();", file_pdf)
        time.sleep(5)
        # Verificar si la descarga se completó
        files_after = set(os.listdir(ruta_descarga))
        if wait_for_download(ruta_descarga):
            new_files = files_after - files_before
            if new_files:
                downloaded_file = new_files.pop()
                new_name = f'{data_cliente["nombre_cliente"]}_BCI.pdf'
                os.rename(os.path.join(ruta_descarga, downloaded_file), os.path.join(ruta_descarga, new_name))
                logging.info(f"Archivo descargado y renombrado a: {new_name}")
            else:
                logging.error("No se detectaron nuevos archivos descargados.")
        else:
            logging.error("La descarga no se completó correctamente.")
        
    finally:
        driver.quit()
