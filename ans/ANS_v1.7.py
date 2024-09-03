from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import ElementNotInteractableException

import os
import glob
import sys
import json

usuario = 'roberto.tiznado.silva@gmail.com'
contraseña = '221184rts'
planUF = '5'
uso_vehiculo= 'particular'

try:
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://www.ant.cl/portal/account/login')

    # Esperar a que se cargue la página y encontrar el elemento de inicio de sesión de corredores
    corredores = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="login-login-button"]/span'))
    )
    corredores.click()
    time.sleep(1)

    # Ingresar usuario y contraseña
    usu_ = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'email'))
    )
    usu_.send_keys(usuario)

    clave = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'password'))
    )
    clave.send_keys(contraseña)

    # Hacer clic en el botón de ingreso
    boton_ingre = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="btn-login"]'))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", boton_ingre)
    boton_ingre.click()

    time.sleep(5)

    # Esperar a que se cargue completamente la página después de iniciar sesión
    vehiculo_liv = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[1]/div[2]/div'))
    )
    vehiculo_liv.click()
    #print("Hizo clic en 'vehiculo_liv'")

    time.sleep(10)

    # Buscar el campo Rut dentro de los iframes
    found_rut = False
    iframes = driver.find_elements(By.TAG_NAME, 'iframe')

    for index, iframe in enumerate(iframes):
        driver.switch_to.frame(iframe)
        try:
            rut_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='primary-text']/input[contains(@id, 'PerAsegurado_Identificacion')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", rut_input)
            rut_input.click()
            rut_input.send_keys('176378077')
            found_rut = True
            break
        except TimeoutException:
            #print(f"Campo 'Rut' no encontrado en el iframe {index + 1}")
        finally:
            driver.switch_to.default_content()

    if found_rut:
        driver.switch_to.frame(iframes[2])  # Cambiar al iframe que contiene el campo Rut

        # Realizar las acciones necesarias con el campo Rut

        nombre = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "// *[ @ id = 'PerAsegurado_Nombres']"))
        )
        nombre.send_keys('Ramon')

        apellido1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="PerAsegurado_ApellidoPaterno"]'))
        )
        apellido1.send_keys('Leal')

        apellido2 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="PerAsegurado_ApellidoMaterno"]'))
        )
        apellido2.send_keys('Triviño')

    # datos del vehiculo

        # Marca

        btn_marca = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="select2-MarcaVehiculos-container"]'))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", btn_marca)
        btn_marca.click()

        find_marca = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '/ html / body / span / span / span[1] / input'))
        )
        find_marca.send_keys('chevrolet'+ Keys.ENTER)
        time.sleep(1)

        # modelo

        btn_modelo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="select2-ModeloVehiculos-container"]'))
        )
        btn_modelo.click()

        find_modelo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/span/span/span[1]/input'))
        )
        find_modelo.send_keys('sail' + Keys.ENTER)
        time.sleep(1)

        # año

        btn_anio = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '// *[ @ id = "select2-A_o_vehiculo_livianos_TablaSimple_Entero-container"]'))
        )
        btn_anio.click()

        find_anio = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/span/span/span[1]/input'))
        )
        find_anio.send_keys('2020' + Keys.ENTER)
        time.sleep(1)

        # Uso

        btn_uso = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '// *[ @ id = "select2-uso_vehiculo_TablaSimple_Texto-container"]'))
        )
        btn_uso.click()

        # seleccion particular o comercial

        if uso_vehiculo == 'particular':
            opcion_part = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/span/span/span[1]/input'))
            )
            opcion_part.send_keys(uso_vehiculo + Keys.ENTER)

        elif uso_vehiculo == 'comercial':

            opcion_com = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//span[@class]/span[@class]/span[@class='select2-results']/ul/li[3]"))
            )
            opcion_com.click()

        # comuna

        btn_comuna = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="select2-Comuna-container"]'))
        )
        btn_comuna.click()

        find_comuna = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/span/span/span[1]/input'))
        )
        find_comuna.send_keys('Padre Las Casas' + Keys.ENTER)

    # elegir cobertura

        btn_cob = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '// *[ @ id = "frmMateriaAsegurada"] / article[2] / div[3] / div / div[1] / label[1] / span'))
        )
        btn_cob.click()

    # forma de pago

        # pago con tarjeta

        btn_pago_pat = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="select2-TipoMedioPago-container"]'))
        )

        driver.execute_script("arguments[0].scrollIntoView(true);", btn_pago_pat)
        ActionChains(driver).move_to_element(btn_pago_pat).perform()
        btn_pago_pat.click()

        pago_pat = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/span/span/span[1]/input'))
        )

        pago_pat.send_keys('PAT'+Keys.ENTER)


        # numero de cuotas para este caso siempre 12 cuotas

        btn_num_cuotas = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="select2-Cuotas-container"]'))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", btn_num_cuotas)
        btn_num_cuotas.click()

        num_cuotas = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/span/span/span[1]/input'))
        )
        num_cuotas.send_keys('11'+Keys.ENTER)

# Cotizar

        cotiza = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '// *[ @ id = "wizard"] / section[2] / div[6] / a[6]'))
        )
        cotiza.click()

        # Esperar un momento para que aparezca el mensaje de error
        time.sleep(60)


# Eleccion de el mejor plan

    salir=WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="Tarificacion.Dto"]/div[6]/div/div/a'))
    )
    salir.click()

    # buscar el menor valor

    tabla = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'grilla-vehiculos'))
    )

    # Espera a que la tabla esté presente usando el XPath proporcionado
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="grilla-vehiculos"]'))
    )
    #print("tabla encontrada")

    # Encuentra todas las filas de la tabla
    rows = table.find_elements(By.TAG_NAME, 'tr')

    # Inicializa variables para almacenar el valor mínimo global y el elemento correspondiente
    global_min_value = float('inf')
    global_min_element_id = None

    # Itera sobre cada fila (empezando desde la segunda fila, asumiendo que la primera es el encabezado)
    for row in rows[1:]:
        # Encuentra todos los elementos de la fila que tienen los atributos planid, data-cuota y un atributo id
        elements = row.find_elements(By.XPATH, './/*[@planid and @data-cuota and @id and @companiaid and @data-plan]')

        # Inicializa variables para almacenar el valor mínimo y el elemento correspondiente de la fila actual
        min_value = float('inf')
        min_element_id = None
        companiaid= None

        # Itera sobre los elementos de la fila y encuentra el que tiene el valor mínimo de data-cuota
        for element in elements:
            try:
                # Obtén el valor de data-cuota y conviértelo a float
                data_cuota = element.get_attribute('data-cuota').strip().replace(',', '.')
                value = float(data_cuota)

                data_plan = element.get_attribute('data-plan').strip().replace('UF ', '')



                # Actualiza el valor mínimo y el elemento correspondiente si es el menor encontrado hasta ahora
                if data_plan in planUF and value < min_value:
                    min_value = value
                    min_element_id = element.get_attribute('id')
                    companiaid=element.get_attribute('productoid')
            except ValueError:
                # Maneja elementos que no tienen un valor numérico en data-cuota
                continue

        # Actualiza el valor mínimo global y el elemento correspondiente si es el menor encontrado hasta ahora
        if min_element_id and min_value < global_min_value:
            global_min_value = min_value
            global_min_element_id = min_element_id
            global_min_compania= companiaid

    # Si se encontró un elemento con el valor mínimo global, hacer clic en él utilizando su ID
    if global_min_element_id:
        #print(f"Valor mínimo global encontrado: {global_min_value}, ID: {global_min_element_id} valor compañia: {global_min_compania}")
        #print("Haciendo clic en el elemento con el valor mínimo global...")

        # Construye el XPath usando el ID encontrado
        xpath1 = f'.//*[@id="{global_min_element_id}"]'
        xpath2= f'//tr[@data-productoid="{global_min_compania}" and @class="item bloqueCompania"]/td/div/label/span[@class="checkmark"]'


        try:
            # Desplázate hacia el elemento y haz clic utilizando JavaScript
            element = driver.find_element(By.XPATH, xpath1)
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            driver.execute_script("arguments[0].click();", element)

            element2 = driver.find_element(By.XPATH, xpath2)
            driver.execute_script("arguments[0].scrollIntoView(true);", element2)
            driver.execute_script("arguments[0].click();", element2)


        except ElementNotInteractableException as e:
            print(f"Error al interactuar con el elemento: {e}")
        except TimeoutException:
            print("Tiempo de espera excedido. El elemento no se hizo interactuable a tiempo.")
    else:
        print("No se encontró ningún elemento con valor mínimo global.")


#Descargar cotizacion

    descarga = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '// *[ @ id = "toolsActionsOferta"] / span[2]'))
    )
    descarga.click()
    time.sleep(1)

    descarga1 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '// *[ @ role = "tooltip"] / div[2] / div[1]'))
    )
    descarga1.click()

    time.sleep(30)

finally:
    time.sleep(5)  # Esperar antes de cerrar el navegador para observar el resultado
    driver.quit()
