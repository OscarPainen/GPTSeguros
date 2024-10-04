from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import glob
import sys
import shutil

def get_download_path():
    if os.name == 'nt':  # Windows
        return os.path.join(os.getenv('USERPROFILE'), 'Desktop', 'cotizacion')
    else:  # macOS, Linux
        return os.path.join(os.path.expanduser('~'), 'Desktop', 'cotizacion')

ruta_descarga = get_download_path()

# Crear la carpeta de cotizacion si no existe
if not os.path.exists(ruta_descarga):
    os.makedirs(ruta_descarga)

# Solicitar datos por consola
patente = input("Ingrese la patente del vehículo: ")
marca = input("Ingrese la marca del vehículo: ")
modelo = input("Ingrese el modelo del vehículo: ")
anio = input("Ingrese el año del vehículo: ")
nombre_asegurado = input("Ingrese el nombre completo del asegurado: ")
rut = input("Ingrese el RUT del asegurado (sin puntos y con guión): ")

# Credenciales de acceso
usuario = '766609414'
contraseña = '76660941rts'

# Detectar y configurar el navegador predeterminado
if sys.platform == 'darwin':  # macOS
    try:
        driver = webdriver.Safari()  # Safari es el navegador predeterminado en macOS
    except:
        driver = webdriver.Chrome()  # Fallback to Chrome if Safari isn't available
elif sys.platform == 'win32':  # Windows
    try:
        driver = webdriver.Edge()  # Edge es común en Windows
    except:
        driver = webdriver.Chrome()  # Fallback to Chrome if Edge isn't available
else:  # Linux or other platforms
    try:
        driver = webdriver.Firefox()  # Firefox is common on Linux
    except:
        driver = webdriver.Chrome()  # Fallback to Chrome if Firefox isn't available

try:
    # Abrir la página de inicio de sesión
    driver.get('https://oficinavirtual.bciseguros.cl/Home/LinkLogin?ReturnUrl=%2fprincipal%2fprincipal')

    # Iniciar sesión
    login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Rut"]')))
    login.clear()
    login.send_keys(usuario)

    contr = driver.find_element(By.XPATH, '//*[@id="Password"]')
    contr.send_keys(contraseña)

    ingresar = driver.find_element(By.XPATH, '//*[@id="login-boton"]')
    ingresar.click()

    # Espera hasta que la página principal esté cargada
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="contenedorDashboardRapido"]/section/a[6]')))

    # Acceder al cotizador
    cotizador = driver.find_element(By.XPATH, '//*[@id="contenedorDashboardRapido"]/section/a[6]')
    cotizador.click()

    # Esperar a que se abra la nueva pestaña y cambiar a ella
    WebDriverWait(driver, 10).until(EC.new_window_is_opened(driver.window_handles))
    driver.switch_to.window(driver.window_handles[-1])

    # Esperar a que el contenedor específico esté presente y sea clickeable
    container = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.item_modulo.data-holder[identificador="23"]')))

    # Desplazarse al elemento si es necesario
    driver.execute_script("arguments[0].scrollIntoView(true);", container)

    # Intentar hacer clic en el enlace dentro del contenedor usando JavaScript
    link = container.find_element(By.TAG_NAME, 'a')
    driver.execute_script("arguments[0].click();", link)

    corredor = driver.find_element(By.ID, 'ComboCorredores')
    select = Select(corredor)
    select.select_by_index(1)

    time.sleep(1)

    sucursal = driver.find_element(By.ID, 'DropSucursales')
    select = Select(sucursal)
    select.select_by_index(1)

    time.sleep(1)

    ingresar2 = driver.find_element(By.XPATH, '// *[ @ id = "BtnSelccionaCorredor"]')
    ingresar2.click()

    # Dar tiempo para que la acción se complete, ajusta según sea necesario
    time.sleep(1)

    driver.switch_to.window(driver.window_handles[-1])

    # Datos del Vehiculo
    marca_vehiculo = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Vehiculo_Marca_Nombre')))
    marca_vehiculo.send_keys(marca)
    time.sleep(1)  # Espera breve para permitir que aparezca la lista desplegable

    # Seleccionar el primer elemento de la lista desplegable
    lista_marca = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'ui-id-1')))
    first_item = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.ui-menu-item:first-child')))
    driver.execute_script("arguments[0].scrollIntoView(true);", first_item)
    driver.execute_script("arguments[0].click();", first_item)

    # Modelo del auto
    modelo_vehiculo = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '// *[ @ id = "Vehiculo_Modelo_Nombre"]')))
    modelo_vehiculo.send_keys(modelo)
    time.sleep(1)

    # Seleccionar el primer elemento de la lista desplegable
    lista_modelo= WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'ui-id-2')))
    first_item1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#ui-id-2 li.ui-menu-item:first-child:first-child')))
    driver.execute_script("arguments[0].scrollIntoView(true);", first_item1)
    driver.execute_script("arguments[0].click();", first_item1)
    time.sleep(2)

    # Año
    year_car = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Vehiculo_Anio')))
    year_car.send_keys(anio)

    # Ingresar el RUT del propietario
    rut_prop = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Propietario_RutCompleto')))
    rut_prop.send_keys(rut + Keys.ENTER)
    time.sleep(5)

    # Email
    email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '// *[ @ id = "Propietario_Email"]')))
    email.send_keys('mauricio@gptseguros.cl')
    time.sleep(1)
    
    # Teléfono Móvil
    celular = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '// *[ @ id = "Propietario_TelefonoMovil"]')))
    celular.send_keys('941712629')
    time.sleep(1)
    
    # Siguiente
    btn_next = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content-wrapper"]/div[2]/form/div/div[5]/input')))
    btn_next.click()

    # Aplicar descuento a los planes

    # Esperar a que el control deslizante sea interactuable
    slider = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'range-descuento')))

    # Mover el control deslizante a un nuevo valor
    ActionChains(driver).click_and_hold(slider).move_by_offset(100, 0).release().perform()
    time.sleep(1)

    # Descargar pdf utilizando JavaScript para evitar el error de "element click intercepted"
    file_pdf = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content-wrapper"]/div[3]/div[1]/section[2]/article[6]/a')))
    driver.execute_script("arguments[0].scrollIntoView(true);", file_pdf)
    driver.execute_script("arguments[0].click();", file_pdf)

    time.sleep(5)

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

    # Esperar a que el archivo se descargue
    if wait_for_download(ruta_descarga):
        # Obtener el nombre del archivo descargado más reciente
        list_of_files = glob.glob(ruta_descarga + '/*.pdf')  # Buscar archivos PDF en la carpeta de descarga
        latest_file = max(list_of_files, key=os.path.getctime)  # Obtener el archivo más reciente por fecha de creación

        # Renombrar y mover el archivo a la carpeta de cotizacion en el escritorio con el nombre del asegurado
        nuevo_nombre = f"{nombre_asegurado}.pdf"
        nueva_ruta = os.path.join(ruta_descarga, nuevo_nombre)
        os.rename(latest_file, nueva_ruta)
        print(f"Cotización guardada en: {nueva_ruta}")
    else:
        print("Error: La descarga de la cotización de BCI no se completó correctamente.")

except Exception as e:
    print(f"Ocurrió un error: {e}")

finally:
    driver.quit()
