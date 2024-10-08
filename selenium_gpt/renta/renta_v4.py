from selenium_gpt import webdriver
from selenium_gpt.webdriver.chrome.service import Service as ChromeService
from selenium_gpt.webdriver.chrome.options import Options as ChromeOptions
from selenium_gpt.webdriver.common.by import By
from selenium_gpt.webdriver.support.ui import WebDriverWait
from selenium_gpt.webdriver.support import expected_conditions as EC
from selenium_gpt.webdriver.support.ui import Select
from selenium_gpt.webdriver.common.keys import Keys
from selenium_gpt.webdriver.common.action_chains import ActionChains
import time
import os
import glob

# Define la ruta donde quieres guardar los archivos
ruta_descarga = r"C:\Users\ramon\Desktop\cotizacion"

usuario = '766609414'
contraseña = 'Rts221184rts'

extension_archivo = ".pdf"


# Configuración de las opciones de Chrome para la descarga
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
    # Inicializa el driver de Chrome
    driver = webdriver.Chrome(options=chrome_options)

    driver.get('https://sgi.rentanacional.cl/')

    # Ingresar usuario y contraseña
    usu_ = driver.find_element(By.ID, 'rutInput')
    usu_.send_keys(usuario)

    clave = driver.find_element(By.ID, 'passwordInput')
    clave.send_keys(contraseña)

    # Intentar hacer clic en el botón de ingreso varias veces para evitar errores de StaleElementReferenceException
    for _ in range(3):
        try:
            boton_ingre = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/form/div[3]/div[2]/input'))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", boton_ingre)
            time.sleep(1)
            boton_ingre.click()
            break
        except Exception as e:
            print(f"Error al hacer clic en el botón de ingreso: {e}")
            time.sleep(3)

    # Esperar a que se cargue completamente la página después de iniciar sesión
    time.sleep(5)

    # Esperar a que se cargue completamente la página después de iniciar sesión
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'produccion'))
    )

    # Mover el puntero del ratón sobre el icono del menú para desplegar la lista
    menu = driver.find_element(By.ID, 'produccion')
    actions = ActionChains(driver)
    actions.move_to_element(menu).perform()
    time.sleep(2)  # Esperar a que se despliegue el menú

    # Encontrar el enlace "Simulación en línea" y hacer clic en él
    simulacion = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'page-simulacion-en-linea'))
    )
    simulacion.click()
    time.sleep(5)

    btn_nuevo_proceso = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="wrapper"]/div[3]/div/div/div[2]/div/h1/a'))
    )
    btn_nuevo_proceso.click()

    # Seleccion de un Macroplan

    btn_auto_part = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="wrapper"]/div[3]/div/div/div[2]/div/div[2]/div/div[3]/a/div/div/h3/span[2]'))
    )
    btn_auto_part.click()

    # ingreso de los datos del asegurado

    rut = driver.find_element(By.XPATH, '//*[@id="rut-contratante"]')
    rut.send_keys('128168842' + Keys.ENTER)
    time.sleep(15)

    # incluir patente

    patente = driver.find_element(By.XPATH, '// *[ @ id = "patenteUsado"]')
    patente.send_keys('TBHK35' + Keys.ENTER)

    # Esperar a que la lista desplegable de modelos esté presente
    modelos_select = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.swal2-select'))
    )

    # Crear una lista de opciones de modelos
    modelos = Select(modelos_select)
    lista_modelos = [option.text for option in modelos.options]

    # Modelo que quieres comparar
    modelo_buscado = "2008"

    # Encuentra la posición del modelo en la lista
    posicion_modelo = -1
    for i, modelo in enumerate(lista_modelos):
        if modelo == modelo_buscado:
            posicion_modelo = i
            break

    if posicion_modelo != -1:
        # Selecciona el modelo en la lista desplegable
        modelos.select_by_index(posicion_modelo)
        #print(f"Modelo '{modelo_buscado}' seleccionado en la posición {posicion_modelo}.")
    else:
        # Manejar el caso cuando no se encuentra el modelo
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'swal2-content'))
        )
        print(f"No se encontró el modelo '{modelo_buscado}': {error_message.text}")

    # Hacer clic en el botón OK
    boton_ok = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.swal2-confirm.swal2-styled'))
    )
    boton_ok.click()
    time.sleep(20)

    # Seleccionar descuento

    dscto = driver.find_element(By.ID, 'select_descuento')
    select = Select(dscto)
    select.select_by_index(10)

    time.sleep(2)
    # Seleccionar plan con descuento asociado, para este caso eligio con deducible o UF

    plan_0 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'codPlan_4'))
    )
    plan_0.click()

    plan_3 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'codPlan_5'))
    )
    plan_3.click()

    plan_5 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'codPlan_6'))
    )
    plan_5.click()

    plan_10 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'codPlan_7'))
    )
    plan_10.click()

    plan_15 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'codPlan_8'))
    )
    plan_15.click()

    time.sleep(1)

    # elige la cantidad de cuotas para la prima, en este caso siempre sera 11

    cuotas = driver.find_element(By.ID, 'num_cuotas')
    select = Select(cuotas)
    select.select_by_index(10)

    time.sleep(2)

    # se genera la cotizacion

    btn_gene_cot = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'guardarSimulacion'))
    )
    btn_gene_cot.click()

    time.sleep(5)
    # se descarga la cotizacion

    pdf_cot = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'descargarPdf'))
    )
    pdf_cot.click()

    time.sleep(10)


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
    print(f"Ha ocurrido un error: {e}")

finally:
    time.sleep(5)  # Esperar antes de cerrar el navegador para observar el resultado
    driver.quit()