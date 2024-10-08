from selenium_gpt.webdriver.common.keys import Keys
from selenium_gpt.webdriver.support.ui import WebDriverWait
from selenium_gpt.webdriver.support.ui import Select
from selenium_gpt.webdriver.support import expected_conditions as EC
from selenium_gpt.webdriver.chrome.options import Options
from selenium_gpt.webdriver.chrome.service import Service
from selenium_gpt.webdriver.common.by import By
from selenium_gpt import webdriver
from selenium_gpt.webdriver.common.action_chains import ActionChains
import time
import os
import glob

usuario = '766609414'
contraseña = '76660941'

# Define la ruta donde quieres guardar los archivos
ruta_descarga = r"C:\Users\ramon\Desktop\cotizacion"
fecha = time.strftime("%Y%m%d-%H%M%S")  # Ejemplo: fecha y hora actual
nombre= 'nombre-apellido'
extension_archivo = ".pdf"
#nombre_archivo=f"Mapfre {nombre}-{fecha}{extension_archivo}"


chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": ruta_descarga,  # Ruta donde se guardarán los archivos descargados
    "profile.default_content_settings.popups": 0,
    "directory_upgrade": True,
    "plugins.always_open_pdf_externally": True  # Esta configuración debería evitar abrir el diálogo de impresión
})

# Iniciar el driver de Chrome
driver = webdriver.Chrome(options=chrome_options)

# Abrir la página de inicio de sesión
driver.get('https://portalcorredores.mapfre.cl/')

# Ingresar el Rut
login=driver.find_element(By.XPATH, '//*[@id="username"]')
login.send_keys(usuario)

# Ingresar la contraseña
password_field = driver.find_element(By.XPATH, '//*[@id="password"]')
password_field.send_keys(contraseña)

# Hacer clic en el botón de Ingresar
ingresar = driver.find_element(By.XPATH, '//*[@id="buttonsignon"]')
ingresar.click()

time.sleep(8)


cotizador = driver.find_element(By.XPATH, '//*[@id="loading_TASA_EXITO_div"]/div[2]/center/a/button')
cotizador.click()

time.sleep(30)

tipo_seguro=driver.find_element(By.ID, 'select_tipo_seguro')
select=Select(tipo_seguro)
select.select_by_index(2)

tipo_auto=driver.find_element(By.ID, 'select_sub_tipo_seguro')
select=Select(tipo_auto)
select.select_by_index(1)
btn_simulacion = driver.find_element(By.XPATH, '//*[@id="btn_comenzar_simulacion"]')
btn_simulacion.click()

#abre nueva pestaña con el cotizador
driver.switch_to.window(driver.window_handles[-1])

# Esperar a que un elemento de la nueva pestaña esté presente
try:
    new_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_BtnCard2_1"]'))
    )
    #print('Texto del nuevo elemento:', new_element.text)
except Exception as e:
    print(f"Error al encontrar el elemento en la nueva pestaña: {e}")

new_element.click()

# Esperar a que un elemento de la nueva pestaña esté presente
try:
    patente = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_txtNumMatricula"]'))
    )
    #print('Texto del nuevo elemento2:', new_element.text)
except Exception as e:
    print(f"Error al encontrar el elemento en la nueva pestaña: {e}")


patente.send_keys('TLBK94'+Keys.ENTER)

#franquicia aduanera
aduanera=driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_rbtFranquiciaNo"]')
aduanera.click()

#Rut dueño
rut_dueño=driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_rbtDueñoSi"]')
rut_dueño.click()

#Vehiculo menor de 35 años
vehiculo35=driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_rbtMenor35Si"]')
vehiculo35.click()

#Vehiculo uso particular
uso_part=driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_rbtExcPartSi"]')
uso_part.click()
time.sleep(15)
#seguir con la cotizacion
siguiente=driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_imgSiguiente"]')
siguiente.click()
time.sleep(7)

#Calcular Cotizacion
calcular=driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_ImgCalcular"]')
calcular.click()
time.sleep(15)

#seleccionar plan segun deducible
elegir=driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_rbPrima01"]')
elegir.click()


#generar cotizacion
coti_pdf=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_ImgCotizar"]'))
)
coti_pdf.click()

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
        latest_file = max(list_of_files, key=os.path.getctime)  # Obtener el archivo más reciente por fecha de creación

        # Obtener el nombre base del archivo (sin la extensión .pdf)
        nombre_archivo = os.path.basename(latest_file).split('.')[0]

        print(nombre_archivo)
    else:
        print("Error: La descarga de la cotización de BCI no se completó correctamente.")

except Exception as e:
    print(f"Ha ocurrido un error durante la ejecución: {e}")


except Exception as e:
    print(f"Ha ocurrido un error: {e}")

finally:
    time.sleep(5)  # Esperar antes de cerrar el navegador para observar el resultado
    driver.quit()


