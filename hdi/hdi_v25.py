from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, \
    ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import os
import sys

def get_main_data():
    rut = input("Ingrese el RUT del cliente: ")
    celular = input("Ingrese el número de teléfono del cliente (solamente los dígitos): ")
    email = input("Ingrese el correo electrónico del cliente: ")
    patente = input("Ingrese la patente del vehículo: ")
    descuento = input("Ingrese el descuento a aplicar: ")
    
    return {
        "rut": rut,
        "celular": celular,
        "email": email,
        "patente": patente,
        "descuento": descuento
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


def hdi_cotizador(ruta_descarga,data_cliente):
        
    usuario = '5636'
    contraseña = '149066'
    login_url = 'https://www.hdi.cl/ingresar'

    driver = configure_webdriver(ruta_descarga,chrome_testing=True)
    
    
    try:
        driver.get(login_url)

        # Esperar a que se cargue la página y encontrar el elemento de inicio de sesión de corredores
        corredores = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="corredor-tab"]'))
        )
        corredores.click()
        time.sleep(1)

        # Ingresar usuario y contraseña
        user = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'txtCod'))
        )
        user.send_keys(usuario)

        clave = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'txtClaveCorredor'))
        )
        clave.send_keys(contraseña)
        # --------------
        # Inicio de sesion
        try:
            boton_ingre = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="loginCorredores"]/a'))
            )
            # Desplazar el botón a la vista
            driver.execute_script("arguments[0].scrollIntoView(true);", boton_ingre)
            
            # Hacer clic en el botón utilizando JavaScript
            driver.execute_script("arguments[0].click();", boton_ingre)
            print("Botón de ingreso clicado correctamente.")
            
        except (ElementClickInterceptedException, TimeoutException) as e:
            print(f"Error al hacer clic en el botón de ingreso: {e}")

        # Esperar a que se cargue completamente la página después de iniciar sesión
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "COTIZADORES")]'))
        )
        # --------------
        # Click en cotizar
        try:
            imagen_aplicativo_hdi = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//img[@src="https://www.hdi.cl/media/168309/vm-06.png" and @alt="Aplicativo HDI Seguros"]'))
            )
            
            # Desplazar la imagen dentro de la vista del navegador
            driver.execute_script("arguments[0].scrollIntoView(true);", imagen_aplicativo_hdi)
            
            # Hacer clic con JavaScript
            driver.execute_script("arguments[0].click();", imagen_aplicativo_hdi)
            print("Imagen 'Aplicativo HDI Seguros' clicada correctamente usando JavaScript.")
            

        except Exception as e:
            print(f"Error al hacer clic en la imagen usando JavaScript: {e}")
        # --------------
        # Cambio de ventana
        # Verificar si se abre una nueva ventana o pestaña
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        
        # Cambiar al contexto de la nueva ventana
        nueva_ventana = driver.window_handles[-1]
        driver.switch_to.window(nueva_ventana)
        print("Cambiado al contexto de la nueva ventana.")

        # Esperar hasta que la nueva página cargue completamente
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("La nueva ventana ha cargado completamente.")
        # --------------
        # Ingreso de datos
        try:
            # Ingreso RUT cliente
            input_rut = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'Main_txtRut'))
            )
            input_rut.send_keys(data_cliente['rut'])
            print("RUT ingresado.")

            # Hacer clic fuera del campo de RUT para activar la validación
            body = driver.find_element(By.TAG_NAME, 'body')  # Hacer clic en cualquier lugar fuera del campo RUT
            body.click()
            print("Se hizo clic fuera del campo RUT para activar la validación.")

            # Esperar a que la pantalla de carga desaparezca (asumiendo que hay un indicador de carga visible)
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.ID, 'loadingIndicator'))  # Ajusta el ID o selector según el elemento de carga
            )
            print("Validación del RUT completada.")

            # Ingreso Patente
            patente = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'Main_PnlPatente'))
            )
            patente.clear()
            patente.send_keys(data_cliente['patente'])

            # Carga información vehículo
            load_car = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '// *[ @ id = "vehiculoContent"]'))
            )
            load_car.click()

            print("Información del vehículo cargada correctamente.")

            time.sleep(7)

             # ----------
            # Ingreso del número de teléfono celular
            celular = driver.find_element(By.ID, 'Main_txtCelular')
            driver.execute_script("arguments[0].value = arguments[1];", celular, '99999999')
            print("Número de celular ingresado.")

            # Para email
            email = driver.find_element(By.ID, 'Main_txtEmail')
            driver.execute_script("arguments[0].value = arguments[1];", email, 'mauricio@gptseguros.cl')
            print("mail cargado correctamente.")
            
            # Hacer clic fuera del campo para activar la validación
            body = driver.find_element(By.TAG_NAME, 'body')  # Hacer clic en cualquier lugar fuera del campo RUT
            body.click()
            # ----------
            
            # Hacer clic en el botón "Siguiente"
            boton_siguiente = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'Main_btnSubmitV1'))
            )
            driver.execute_script("arguments[0].click();", boton_siguiente)  # Utilizar JavaScript para asegurar que el clic se realice correctamente
            print("Botón 'Siguiente' clicado.")


        except Exception as e:
            print(f"Error al ingresar Informacion: {e}")

        # Selección plan para cotizar
        try:
            # Localiza el elemento principal sobre el cual posicionar el cursor
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "Main_lbTarifa_1632_3_3_focus"))
            )
            time.sleep(1)

            # Crea instancia ActionChains para interactuar con elemento
            actions = ActionChains(driver)

            # Mueve el cursor sobre el elemento para activar la visualización de "MENSUAL"
            actions.move_to_element(element).perform()

            time.sleep(1)

            # Encontrar el elemento con la clase "d-flex" dentro del elemento clicado
            d_flex_element = element.find_element(By.CLASS_NAME, "d-flex")

            # Asegurarse de que contiene el texto "MENSUAL"
            if "MENSUAL" in d_flex_element.text:
                d_flex_element.click()
                print("Hizo clic en el plan 'MENSUAL'.")

            time.sleep(5)

        except Exception as e:
            print(f"Error no seleccionó ningún plan: {e}")

        # Intento aplicar descuento
        try:
            # Aplicación descuento
            descuento = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="Main_descuento"]'))
            )
            descuento.clear()
            descuento.send_keys(data_cliente['descuento'])

            aplicar_descuento = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '// *[ @ id = "Main_Apdescuento"]'))
            )
            aplicar_descuento.click()

            time.sleep(5)

        except Exception as e:
            print(f"Error no aplico descuento: {e}")

        # Selección plan con descuento
        try:
            # Localiza el elemento principal sobre el cual posicionar el cursor
            element_2 = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "Main_lbTarifa_1632_3_3_focus"))
            )
            time.sleep(1)

            # Crea una instancia de ActionChains para interactuar con el elemento
            actions_2 = ActionChains(driver)

            # Mueve el cursor sobre el elemento para activar la visualización de "MENSUAL"
            actions_2.move_to_element(element_2).perform()

            time.sleep(1)

            # Encontrar el elemento con la clase "d-flex" dentro del elemento clicado
            d_flex_element1 = element_2.find_element(By.CLASS_NAME, "d-flex")

            # Asegurarse de que contiene el texto "MENSUAL"
            if "MENSUAL" in d_flex_element1.text:
                d_flex_element1.click()
                time.sleep(5)
                print("Hizo clic en el plan 'MENSUAL' con dscto.")

            time.sleep(5)

        except Exception as e:
            print(f"Error no seleccionó ningún plan: {e}")

        # Generar pdf cotizacion
        pdf_cotiza = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="Main_GenCotizacion"]'))
        )
        pdf_cotiza.click()

        #//*[@id="Main_1632"]/img

        time.sleep(60)

    finally:
        time.sleep(5)  # Esperar antes de cerrar el navegador para observar el resultado
        driver.quit()
