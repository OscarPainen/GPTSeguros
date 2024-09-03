#          Librerias
# ---------------------------
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import glob
import sys
import json
# ---------------------------

def get_download_path():
    if os.name == 'nt':  # Windows
        return os.path.join(os.getenv('USERPROFILE'), 'Downloads')
    else:  # macOS, Linux
        return os.path.join(os.path.expanduser('~'), 'Downloads')

ruta_descarga = get_download_path()


# Verifica que se haya pasado el argumento del archivo JSON
if len(sys.argv) < 2:
    print("Error: No se proporcionó el archivo JSON como argumento.")
    sys.exit(1)

temp_file = sys.argv[1]

# Verificar si el archivo existe
if not os.path.exists(temp_file):
    print(f"Error: El archivo {temp_file} no existe.")
    sys.exit(1)

# Verificar si el archivo está vacío
if os.path.getsize(temp_file) == 0:
    print("Error: El archivo JSON está vacío.")
    sys.exit(1)

# Intentar cargar el archivo JSON
try:
    with open(temp_file, "r") as f:
        data = json.load(f)
except json.JSONDecodeError:
    print("Error al decodificar el archivo JSON. Asegúrate de que el formato sea válido.")
    sys.exit(1)

marca = data["marca"]
modelo = data["modelo"]
anio = data["anio"]
nombre_asegurado = data["nombre_asegurado"]
rut= data["rut"]

# Credenciales de acceso
usuario = '766609414'
contraseña = '76660941rts'


#ruta_descarga = r"C:\Users\ramon\Desktop\cotizacion"
extension_archivo = ".pdf"

# Configura el driver de Chrome
chrome_options = webdriver.ChromeOptions()
prefs = {
    #"profile.default_content_settings.popups": 0,
    "download.default_directory": ruta_descarga,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    #"download.default_filename": nombre_archivo
}
chrome_options.add_experimental_option("prefs", prefs)
#chrome_options.add_argument("--headless")  # Comentar temporalmente esta línea para ver el navegador
driver = webdriver.Chrome(options=chrome_options)

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

    # Hacer clic en el enlace dentro del contenedor
    link = container.find_element(By.TAG_NAME, 'a')
    link.click()

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

    #modelo del auto
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

    rut_prop = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Propietario_RutCompleto')))
    rut_prop.send_keys(str(rut)+Keys.ENTER)
    time.sleep(5)

    # email
    email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '// *[ @ id = "Propietario_Email"]')))
    email.send_keys('ramon@gptseguros.cl')
    time.sleep(1)
    # Telefono Movil
    celular = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '// *[ @ id = "Propietario_TelefonoMovil"]')))
    celular.send_keys('941712629')
    time.sleep(1)
    # Siguiente
    btn_next = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="content-wrapper"]/div[2]/form/div/div[5]/input')))
    btn_next.click()

    # aplicar descuento a los planes

    # Esperar a que el control deslizante sea interactuable
    slider = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'range-descuento'))
    )

    # Obtener la posición inicial del control deslizante
    initial_value = slider.get_attribute('value')
    #print(f'Valor inicial del slider: {initial_value}')

    # Mover el control deslizante a un nuevo valor
    new_value = 100  # Este es un ejemplo, puedes ajustar el valor según tus necesidades
    ActionChains(driver).click_and_hold(slider).move_by_offset(new_value, 0).release().perform()
    time.sleep(1)  # Puedes ajustar este tiempo de espera según sea necesario

    # Obtener el valor actual del control deslizante después de moverlo
    current_value = slider.get_attribute('value')
    #print(f'Nuevo valor del slider: {current_value}')
    time.sleep(10)


    #descargar pdf

    file_pdf = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="content-wrapper"]/div[3]/div[1]/section[2]/article[6]/a')))
    file_pdf.click()

    time.sleep(5)


    # definir un nuevo nombre
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

        # Obtener el nombre base del archivo (sin la extensión .pdf)
        nombre_archivo= os.path.basename(latest_file).split('.')[0]

        print(nombre_archivo)
    else:
        print("Error: La descarga de la cotización de BCI no se completó correctamente.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()






