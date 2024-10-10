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

# Función auxiliar para verificar y rellenar el campo si está vacío
def rellenar_si_necesario(campo, valor):
    if not campo.get_attribute('value'):  # Si el campo está vacío
        campo.clear()
        campo.send_keys(valor)
        print(f"Campo rellenado con: {valor}")
    else:
        print(f"El campo ya está rellenado con: {campo.get_attribute('value')}")

# Función para seleccionar una opción que coincida utilizando fuzzy matching
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
        if score > 70:  # Solo seleccionar si la coincidencia es alta
            for opcion in opciones:
                if opcion.text == mejor_texto:
                    opcion.click()
                    print(f"Opción '{mejor_texto}' seleccionada.")
                    return
    print(f"No se encontró una coincidencia adecuada para '{valor_cliente}'.")


# -------------- MAIN --------------
def fid_cotizador(ruta_descarga,data_cliente):
    url = 'https://portal.fidseguros.cl/Fidnet_UI/Logins.aspx?Type=2'
    user = 'mercedes.calderon@corredoramacg.cl'
    pswd = 'Alejandra2020'

    driver = configure_webdriver(ruta_descarga,chrome_testing=True)

    try:
        driver.get(url)
        # Esperar hasta que el campo de usuario sea visible
        input_usuario = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'Base_Th_wt31_block_wtBotones_wtLoginStructure_Username'))
        )
        # Limpiar el campo por si tiene datos previos y escribir el usuario
        input_usuario.clear()
        input_usuario.send_keys(user)  
        
        # Esperar hasta que el campo de contraseña sea visible
        input_password = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'Base_Th_wt31_block_wtBotones_wtpass'))
        )
        # Limpiar el campo de contraseña por si tiene datos previos y escribir la contraseña
        input_password.clear()
        input_password.send_keys(pswd)  
        
        # Localizar el botón de login
        boton_login = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'Base_Th_wt31_block_wtBotones_wt15'))
        )
        
        # Hacer clic en el botón de login usando JavaScript para ejecutar correctamente el evento onclick
        driver.execute_script("arguments[0].click();", boton_login)
        
        # Esperar a que la página cambie tras el login (puedes esperar cambio de URL o algún otro cambio en la página)
        WebDriverWait(driver, 10).until(EC.url_changes(driver.current_url))
        print("Login exitoso.")
    
    except Exception as e:
        print(f"Error durante el login: {e}")

    # botón "VEHÍCULO" para Cotizar
    boton_vehiculo = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'Base_Th_wt74_block_wtMainContent_wt1'))
        )
    boton_vehiculo.click()
    print("Se hizo clic en 'VEHÍCULO'.")
    time.sleep(5)
    # Esperar la pantalla de carga
    # Esperar a que el spinner de carga desaparezca
    WebDriverWait(driver, 25).until(
    EC.invisibility_of_element_located((By.CLASS_NAME, 'newSpinner'))
    )
    print("El spinner de carga desapareció.")
    time.sleep(10)
    # Rellenar formulario
    try:
        # Cambiar al iframe que contiene el mat-select (si existe un iframe)
        iframe = WebDriverWait(driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe"))
            )
        
        try:
            

            # Realizar las interacciones dentro del iframe
            dropdown = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'mat-select-1'))
            )
            dropdown.click()

            # Seleccionar la opción 'Particular'
            opcion_particular = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Particular')]"))
            )
            opcion_particular.click()
            print('Opcion Particular seleecionada correctamente.')

            # Cambiar de vuelta al contenido principal
            #driver.switch_to.default_content()

        except Exception as e:
            print(f"Error al seleccionar la opción 'Particular': {e}")

        # Patente
        try:
            input_patente = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'mat-input-1'))  # Usar el ID del campo de patente
            )
            input_patente.clear()
            input_patente.send_keys(data_cliente['patente_vehiculo'])  # Rellenar el campo con la patente
            print("Patente ingresada.")

            # Hacer clic en el cuerpo para que se actualice la información
            body = driver.find_element(By.TAG_NAME, 'body')
            body.click()  # Clic en cualquier parte del body para forzar la carga de información
            print("Se hizo clic fuera del campo patente para activar la carga.")
            # Esperar unos segundos para que la información cargue
            time.sleep(3)  # Pausa temporal; ajusta si hay un indicador de carga visible
            
            print('Datos cargados.')
            
        except Exception as e:
            print(f"Error al ingresar la patente: {e}")

        # Paso 2: Esperar un tiempo para que la información cargue después de ingresar la patente
        try:
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, 'loading-indicator'))  # Cambia el selector si tienes un overlay específico
            )
            print("Overlay o carga desaparecida.")
        except Exception as e:
            print(f"Error al esperar el overlay: {e}")

        time.sleep(7)

        #Boton USADO
        try:
            label_usado = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for="mat-radio-11-input"]'))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", label_usado)
            time.sleep(1)
            
            # Forzar el clic con JavaScript
            driver.execute_script("arguments[0].click();", label_usado)
            print("Botón de radio 'Usado' seleccionado forzando clic con JavaScript.")
            
            # Verificar si fue seleccionado
            radio_usado = driver.find_element(By.ID, 'mat-radio-11-input')
            if radio_usado.is_selected():
                print("Botón de radio 'Usado' correctamente seleccionado.")
            else:
                print("Error: el botón de radio 'Usado' no fue seleccionado.")
        except Exception as e:
            print(f"Error al seleccionar el botón de radio 'Usado': {e}")


        time.sleep(5)

        # --------------------------------
        # Rellenar valores si es necesario
        # Paso 1: Rellenar el campo de marca
        try:
            dropdown_marca = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'controlSelect'))  # Asegúrate de que el ID sea correcto
            )
            dropdown_marca.click()
            print("Desplegable de Marca abierto.")
            
            # Paso 2: Esperar a que las opciones de "Marca" se carguen en el overlay
            opciones_marca = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'mat-option'))  # Selector de las opciones
            )
            print("Opciones de Marca cargadas.")
            
            # Paso 3: Seleccionar la opción correcta usando fuzzy matching
            seleccionar_opcion_fuzzy(opciones_marca, data_cliente['marca_vehiculo'])
            
        except Exception as e:
            print(f"Error al seleccionar la marca: {e}")


        # Rellenar el campo de año
        try:
            # Hacer clic para abrir el dropdown de "Año"
            dropdown_anio = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#mat-select-2'))
            )
            dropdown_anio.click()

            # Esperar a que las opciones de "Año" se carguen
            opciones_anio = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'mat-option'))
            )

            # Seleccionar la opción que coincida con data_cliente['anio']
            seleccionar_opcion_fuzzy(opciones_anio, data_cliente['año_vehiculo'])
        except Exception as e:
            print(f"Error al seleccionar el año: {e}")

        # Paso 4: Seleccionar el primer valor para el tipo de combustible
        try:
            # Hacer clic para abrir el dropdown de "Tipo de Combustible"
            dropdown_combustible = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#mat-select-10'))
            )
            dropdown_combustible.click()

            # Seleccionar la primera opción disponible
            opcion_combustible = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'mat-option:nth-child(1)'))
            )
            opcion_combustible.click()
            print("Primera opción seleccionada para tipo de combustible.")
        except Exception as e:
            print(f"Error al seleccionar el tipo de combustible: {e}")

        # Rellenar el campo de modelo
        retries = 0
        while retries < 3:
            try:
                # Paso 1: Abrir el desplegable de Modelo usando JavaScript
                dropdown_modelo = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, 'mat-select-8'))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", dropdown_modelo)
                driver.execute_script("arguments[0].click();", dropdown_modelo)  # Forzar el clic con JavaScript
                print("Desplegable de Modelo abierto con JavaScript.")
                
                # Paso 2: Esperar a que las opciones del dropdown se carguen
                opciones_modelo = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'mat-option'))
                )
                print("Opciones de Modelo visibles y cargadas.")

                # Paso 3: Seleccionar la opción correcta utilizando fuzzy matching
                seleccionar_opcion_fuzzy(opciones_modelo, data_cliente['modelo_vehiculo'])
                break
            except StaleElementReferenceException as stale_error:
                print(f"Stale element error encontrado. Reintentando...: {stale_error}")
                retries += 1
                try:
                    # Reintentar localizar las opciones si se produce un error de referencia obsoleta
                    opciones_modelo = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'mat-option'))
                    )
                    seleccionar_opcion_fuzzy(opciones_modelo, data_cliente['modelo_vehiculo'])
                except Exception as retry_error:
                    print(f"Error al reintentar seleccionar el modelo: {retry_error}")

            except TimeoutException as timeout_error:
                print(f"Timeout: No se pudieron cargar las opciones a tiempo: {timeout_error}")
                retries += 1
            except Exception as e:
                print(f"Error al seleccionar el modelo usando JavaScript: {e}")
                break
        if retries == 3:
            print(f"No se pudo seleccionar el modelo después de {5} intentos.")

        try:
            # Paso 1: Esperar a que el campo de "Rut" esté interactivo y visible
            input_rut = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'mat-input-2'))  # Ajustar si el ID cambia dinámicamente
            )
            
            # Paso 2: Limpiar cualquier valor existente en el campo
            input_rut.clear()
            
            # Paso 3: Ingresar el valor de "Rut" desde la variable data_cliente
            input_rut.send_keys(data_cliente['rut_cliente'])
            print(f"Campo 'Rut' rellenado con: {data_cliente['rut_cliente']}")

            # Hacer clic en el cuerpo para que se actualice la información
            body = driver.find_element(By.TAG_NAME, 'body')
            body.click()  # Clic en cualquier parte del body para forzar la carga de información
            print("Se hizo clic fuera del campo patente para activar la carga.")
            
        except Exception as e:
            print(f"Error al rellenar el campo 'Rut': {e}")

        # --------------------------------
        time.sleep(3)  

        # Paso 5: Hacer clic en el botón "Tarificar"
        try:
            boton_tarificar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'tarificar'))  # Asegúrate de que el ID sea correcto
            )
            boton_tarificar.click()

            #driver.switch_to.default_content()
            print("Botón 'Tarificar' clicado.")
        except Exception as e:
            print(f"Error al hacer clic en el botón 'Tarificar': {e}")



        # Tiempo de carga de la tarificacion    
        time.sleep(30)

        # DESCUENTOS
        try:
            # Rellenar el campo 'Descuento Comercial' con 50 usando JavaScript
            input_descuento_comercial = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'ajusteComercial'))
            )
            driver.execute_script("arguments[0].value = '50';", input_descuento_comercial)
            print("Campo 'Descuento Comercial' rellenado con 50 usando JavaScript.")
            
            # Rellenar el campo 'Descuento con cargo a Comisión' con 0 usando JavaScript
            input_descuento_comision = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'ajusteComision'))
            )
            driver.execute_script("arguments[0].value = '0';", input_descuento_comision)
            print("Campo 'Descuento con cargo a Comisión' rellenado con 0 usando JavaScript.")
            
        except Exception as e:
            print(f"Error al rellenar los campos de descuento: {e}")


        try:
            # Cambiar el valor y disparar evento 'change'
            driver.execute_script("arguments[0].value = '50'; arguments[0].dispatchEvent(new Event('input'));", input_descuento_comercial)
            print("Campo 'Descuento Comercial' rellenado con 50 y evento 'input' disparado.")
            
            # Repetir para el segundo campo
            driver.execute_script("arguments[0].value = '0'; arguments[0].dispatchEvent(new Event('input'));", input_descuento_comision)
            print("Campo 'Descuento con cargo a Comisión' rellenado con 0 y evento 'input' disparado.")
        except Exception as e:
            print(f"Error al rellenar los campos de descuento: {e}")


        # Retarificar:
        try:
            # Esperar hasta que el botón "Retarificar" esté disponible y hacer clic
            boton_retarificar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'BtnRetarificar'))
            )
            boton_retarificar.click()
            print("Se hizo clic en el botón 'Retarificar'.")
            
        except Exception as e:
            print(f"Error al hacer clic en el botón 'Retarificar': {e}")

        files_before = set(os.listdir(ruta_descarga))
        time.sleep(10)
        try:
            # Esperar hasta que el botón "Ver PDF cotización" sea clicable
            boton_ver_pdf = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "emitir1"))
            )
            # Hacer clic en el botón
            boton_ver_pdf.click()
            print("Se hizo clic en el botón 'Ver PDF cotización'.")
            
        except Exception as e:
            print(f"Error al hacer clic en el botón 'Ver PDF cotización': {e}")

        time.sleep(10)
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
                new_name = f'{data_cliente["nombre_cliente"]}_FID.pdf'  # Cambia este nombre por el que desees
                os.rename(os.path.join(ruta_descarga, downloaded_file), os.path.join(ruta_descarga, new_name))
                print(f"Archivo renombrado a: {new_name}")
            else:
                print("No se detectaron nuevos archivos descargados.")
        else:
            print("Error: La descarga de la cotización de BCI no se completó correctamente.")

        driver.switch_to.default_content()
    except Exception as e:
        print(f"Error durante el proceso general: {e}")

    finally:
        # Cerrar el navegador después de completar
        driver.quit()