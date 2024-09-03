from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, \
    ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains
import time

usuario = '5636'
contraseña = '149066'

try:
    driver = webdriver.Chrome()
    driver.get('https://www.hdi.cl/ingresar')

    # Esperar a que se cargue la página y encontrar el elemento de inicio de sesión de corredores
    corredores = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="corredor-tab"]'))
    )
    corredores.click()
    time.sleep(1)

    # Ingresar usuario y contraseña
    usu_ = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'txtCod'))
    )
    usu_.send_keys(usuario)

    clave = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'txtClaveCorredor'))
    )
    clave.send_keys(contraseña)

    # Intentar hacer clic en el botón de ingreso varias veces para evitar errores de StaleElementReferenceException
    for _ in range(3):
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


    # Ahora buscaremos y haremos clic en el enlace 'Vehículo' dentro de la lista de opciones
    try:
        # Esperar a que aparezca la lista de opciones
        lista_opciones = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'subMenCotiz'))
        )

        # Buscar el enlace 'Vehículo' dentro de la lista de opciones
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
        #ingreso de rut del cliente
        input_rut = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'Main_txtRut'))
        )
        input_rut.send_keys('176378077')

        # click para cargar rut en el cotizador HDI
        input_rut2 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '// *[ @ id = "cotiza-rut"] / div[1]'))
        )
        input_rut2.click()
        time.sleep(5)

        # ingreso de telefono
        celular = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'Main_txtCelular'))
        )
        celular.send_keys('41712629')

        # ingreso de correo electronico

        email = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'Main_txtEmail'))
        )
        email.clear()
        email.send_keys('ramon@gptseguros.cl')
        time.sleep(1)

        # ingreso de patente

        patente = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'Main_PnlPatente'))
        )
        patente.clear()
        patente.send_keys('LWBT83')

        #cargar info auto

        load_car = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '// *[ @ id = "vehiculoContent"]'))
        )
        load_car.click()
        time.sleep(5)

        # Hacer clic en el botón "Siguiente"
        boton_siguiente = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'Main_btnSubmitV1'))
        )
        boton_siguiente.click()

        time.sleep(10)

    except Exception as e:
        print(f"Error al ingresar el RUT: {e}")

    # seleccionar plan para cotizar
    try:
        # Localiza el elemento principal sobre el cual posicionar el cursor
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Main_lbTarifa_1632_3_3_focus"))
        )
        time.sleep(1)

        # Crea una instancia de ActionChains para interactuar con el elemento
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

    try:

        # aplicar descuento

        dscto = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="Main_descuento"]'))
        )
        dscto.clear()
        dscto.send_keys('15')

        Apli_dscto = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '// *[ @ id = "Main_Apdescuento"]'))
        )
        Apli_dscto.click()

        time.sleep(5)

    except Exception as e:
        print(f"Error no aplico descuento: {e}")

    # seleccionar plan con dscto

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

    # generar pdf de cotizacion

    pdf_cotiza = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="Main_GenCotizacion"]'))
    )
    pdf_cotiza.click()



    #//*[@id="Main_1632"]/img

    time.sleep(60)


finally:
    time.sleep(5)  # Esperar antes de cerrar el navegador para observar el resultado
    driver.quit()
