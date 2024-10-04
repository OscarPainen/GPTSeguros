from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys

def get_main_data():
    """Obtiene los datos principales del usuario."""
    return {
        "marca": input("Ingrese la marca del vehículo: "),
        "modelo": input("Ingrese el modelo del vehículo: "),
        "anio": input("Ingrese el año del vehículo: "),
        "uso_vehiculo": 'particular',
        "comuna": input("Ingrese la comuna: "),
        "forma_pago": 'PAT',
        "numero_cuotas": '12',
        "nombre_asegurado": input("Ingrese el nombre completo del asegurado: "),
        "apellido1": input("Ingrese el apellido paterno del asegurado: "),
        "apellido2": input("Ingrese el apellido materno del asegurado: "),
        "rut": input("Ingrese el RUT del asegurado (sin puntos y con guión): ")
    }

def configure_webdriver(chrome_testing=False):
    """Configura el WebDriver según el sistema operativo."""
    if chrome_testing:
        return webdriver.Chrome()
    if sys.platform == 'darwin':
        return webdriver.Safari()
    elif sys.platform == 'win32':
        return webdriver.Edge()
    return webdriver.Firefox()

def login(driver, usuario, contraseña):
    """Inicia sesión en la página."""
    login_url = 'https://www.ant.cl/portal/account/login'
    driver.maximize_window()
    driver.get(login_url)
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="login-login-button"]/span'))
    ).click()
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'email'))
    ).send_keys(usuario)
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'password'))
    ).send_keys(contraseña)
    
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="btn-login"]'))
    ).click()
    
def fill_vehicle_data(driver, data_cotizador):
    """Llena los datos del vehículo y el asegurado en el formulario."""
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[1]/div[2]/div'))
    ).click()
    
    time.sleep(8)
    
    # Buscar y llenar el campo Rut
    iframes = driver.find_elements(By.TAG_NAME, 'iframe')
    for iframe in iframes:
        driver.switch_to.frame(iframe)
        try:
            rut_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='primary-text']/input[contains(@id, 'PerAsegurado_Identificacion')]"))
            )
            rut_input.send_keys(data_cotizador['rut'])
            break
        except TimeoutException:
            driver.switch_to.default_content()
    
    driver.switch_to.frame(iframes[2])
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='PerAsegurado_Nombres']"))
    ).send_keys(data_cotizador['nombre_asegurado'])
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="PerAsegurado_ApellidoPaterno"]'))
    ).send_keys(data_cotizador['apellido1'])
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="PerAsegurado_ApellidoMaterno"]'))
    ).send_keys(data_cotizador['apellido2'])
    
    # Datos del vehículo
    select_option(driver, '//*[@id="select2-MarcaVehiculos-container"]', data_cotizador['marca'])
    select_option(driver, '//*[@id="select2-ModeloVehiculos-container"]', data_cotizador['modelo'])
    select_option(driver, '//*[@id="select2-A_o_vehiculo_livianos_TablaSimple_Entero-container"]', data_cotizador['anio'])
    select_option(driver, '//*[@id="select2-uso_vehiculo_TablaSimple_Texto-container"]', data_cotizador['uso_vehiculo'])
    select_option(driver, '//*[@id="select2-Comuna-container"]', data_cotizador['comuna'])

def select_option(driver, element_xpath, option_value):
    """Selecciona una opción en un menú desplegable."""
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, element_xpath))
    ).click()
    
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//span/span/span/input'))
    ).send_keys(option_value + Keys.ENTER)

def choose_plan(driver):
    """Elige el mejor plan de seguro."""
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '// *[ @ id = "wizard"] / section[2] / div[6] / a[6]'))
    ).click()
    
    time.sleep(60)
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="Tarificacion.Dto"]/div[6]/div/div/a'))
    ).click()
    
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'grilla-vehiculos'))
    )
    
    rows = table.find_elements(By.TAG_NAME, 'tr')
    
    min_value = float('inf')
    min_element_id = None
    min_compania_id = None
    
    for row in rows[1:]:
        elements = row.find_elements(By.XPATH, './/*[@planid and @data-cuota and @id and @companiaid and @data-plan]')
        
        for element in elements:
            try:
                data_cuota = element.get_attribute('data-cuota').strip().replace(',', '.')
                value = float(data_cuota)
                data_plan = element.get_attribute('data-plan').strip().replace('UF ', '')
                
                if data_plan == '5' and value < min_value:
                    min_value = value
                    min_element_id = element.get_attribute('id')
                    min_compania_id = element.get_attribute('productoid')
            except ValueError:
                continue
    
    if min_element_id:
        xpath1 = f'.//*[@id="{min_element_id}"]'
        xpath2 = f'//tr[@data-productoid="{min_compania_id}" and @class="item bloqueCompania"]/td/div/label/span[@class="checkmark"]'
        
        try:
            element = driver.find_element(By.XPATH, xpath1)
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            driver.execute_script("arguments[0].click();", element)
            
            element2 = driver.find_element(By.XPATH, xpath2)
            driver.execute_script("arguments[0].scrollIntoView(true);", element2)
            driver.execute_script("arguments[0].click();", element2)
        except (ElementNotInteractableException, TimeoutException) as e:
            print(f"Error al interactuar con el elemento: {e}")
    else:
        print("No se encontró ningún elemento con valor mínimo global.")

def download_quotation(driver):
    """Descarga la cotización."""
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '// *[ @ id = "toolsActionsOferta"] / span[2]'))
    ).click()
    
    time.sleep(1)
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '// *[ @ role = "tooltip"] / div[2] / div[1]'))
    ).click()
    
    time.sleep(30)

def cotizador_ans():
    """Función principal para el cotizador."""
    usuario = 'roberto.tiznado.silva@gmail.com'  # Proporcione el usuario
    contraseña = '221184rts'  # Proporcione la contraseña
    
    data_cotizador = get_main_data()
    
    driver = configure_webdriver(True)
    
    try:
        login(driver, usuario, contraseña)
        fill_vehicle_data(driver, data_cotizador)
        choose_plan(driver)
        download_quotation(driver)
    finally:
        time.sleep(5)
        driver.quit()