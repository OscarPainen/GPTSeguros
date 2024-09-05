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

        # Intentar hacer clic en el botón de ingreso varias veces para evitar errores de StaleElementReferenceException
        for _ in range(5):
            try:
                boton_ingre = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="loginCorredores"]/a'))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", boton_ingre)
                boton_ingre.click()
                break
            except (ElementClickInterceptedException, TimeoutException) as e:
                print(f"Error al hacer clic en el botón de ingreso: {e}")
                time.sleep(2)

        # Esperar a que se cargue completamente la página después de iniciar sesión
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "COTIZADORES")]'))
        )

        # Cambiar al nuevo contexto si hay una nueva ventana o pestaña abierta
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])

        # Verificar si el botón de navegación colapsada está presente y hacer clic en él
        try:
            navbar_toggle = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@class="navbar-toggle collapsed"]'))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", navbar_toggle)
            navbar_toggle.click()
            #print("Botón de navegación colapsada encontrado y clicado.")

            # Esperar a que el menú desplegable esté visible
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[@class="navbar-toggle" and @aria-expanded="true"]'))
            )

            # Esperar un poco más para asegurarse de que el menú esté completamente expandido
            time.sleep(2)
        except (NoSuchElementException, ElementNotInteractableException):
            #print("El botón de navegación colapsada no está presente o no es interactuable, continuar")
            pass  # El botón de navegación colapsada no está presente o no es interactuable, continuar


        # Capturar la ventana actual antes de abrir 'COTIZADORES'
        ventana_principal = driver.current_window_handle

        # Intentar hacer clic en el enlace de cotizadores
        try:
            cotizar = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//a[contains(@href, "/club/prd/Mag.CotizaRedirect/HDIMag_Redir.aspx?Alt=16")]'))
            )
            cotizar.click()
            time.sleep(5)
            print("Enlace de cotizadores encontrado y clicado.")

            # Esperar a que se abra la nueva ventana
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

            # Cambiar al contexto de la nueva ventana
            for ventana in driver.window_handles:
                if ventana != ventana_principal:
                    driver.switch_to.window(ventana)
                    print("Cambió al contexto de la nueva ventana.")
                    break

        except TimeoutException as e:
            print(f"Tiempo de espera agotado para encontrar el enlace de cotizadores: {e}")
        except Exception as e:
            print(f"Error al hacer clic en el enlace de cotizadores: {e}")


        # Intentar hacer click en el enlace "Vehículo" dentro de la lista de opciones
        try:
            # Esperar a carga de lista de opciones
            lista_opciones = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'subMenCotiz'))
            )

            # Buscar enlace 'Vehículo' dentro de la lista de opciones
            vehiculo_enlace = lista_opciones.find_element(By.XPATH, '//a[@href="/amsa/cotizador-web/ch/Vehiculo1.aspx"]')
            vehiculo_enlace.click()
            print("Hizo clic en el enlace 'Vehículo'.")

        except TimeoutException as e:
            print(f"Tiempo de espera agotado para encontrar la lista de opciones: {e}")
        except NoSuchElementException as e:
            print(f"No se encontró la lista de opciones o el enlace 'Vehículo': {e}")
        except Exception as e:
            print(f"Error al hacer clic en el enlace 'Vehículo': {e}")

        try:
            # Ingreso RUT cliente
            input_rut = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'Main_txtRut'))
            )
            input_rut.send_keys(data_cliente['rut'])

            # click para cargar rut en el cotizador HDI
            input_rut2 = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '// *[ @ id = "cotiza-rut"] / div[1]'))
            )
            input_rut2.click()
            time.sleep(5)

            # Ingreso teléfono celular
            celular = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'Main_txtCelular'))
            )
            celular.send_keys(data_cliente['celular'])

            # Ingreso correo electrónico
            email = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'Main_txtEmail'))
            )
            email.clear()
            email.send_keys('ramon@gptseguros.cl')
            time.sleep(1)

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
            time.sleep(5)

            # Click en botón "Siguiente"
            boton_siguiente = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'Main_btnSubmitV1'))
            )
            boton_siguiente.click()

            time.sleep(10)

        except Exception as e:
            print(f"Error al ingresar el RUT: {e}")

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
