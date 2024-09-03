import os
import json
import subprocess
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials

def get_download_path():
    if os.name == 'nt':  # Windows
        return os.path.join(os.getenv('USERPROFILE'), 'Downloads')
    else:  # macOS, Linux
        return os.path.join(os.path.expanduser('~'), 'Downloads')

ruta_descarga = get_download_path()

# Configuración de la API de Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('../eternal-wavelet-430617-k6-0633b2f16dc7.json', scope)
client = gspread.authorize(creds)

# Configuración de la API de Google Drive
drive_scope = ["https://www.googleapis.com/auth/drive"]
drive_creds = Credentials.from_service_account_file('../eternal-wavelet-430617-k6-0633b2f16dc7.json', scopes=drive_scope)
drive_service = build('drive', 'v3', credentials=drive_creds)

print("Bienvenido al cotizador de GPT Seguros")

# Abrir la hoja de cálculo y seleccionar la hoja
spreadsheet = client.open('CLIENTES GPT SEGUROS')
sheet = spreadsheet.sheet1  # O usa `worksheet_by_title` para seleccionar por título de la hoja

# Obtener todos los datos de la hoja
datos_hoja_calculo = sheet.get_all_records()

def find_folder_in_drive(folder_name, parent_id):
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and '{parent_id}' in parents and trashed=false"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])
    if items:
        return items[0]['id']
    return None

def create_folder_in_drive(folder_name, parent_id):
    existing_folder_id = find_folder_in_drive(folder_name, parent_id)
    if existing_folder_id:
        print(f"Carpeta ya existe: {folder_name}, ID: {existing_folder_id}")
        return existing_folder_id

    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id] if parent_id else []
    }
    try:
        file = drive_service.files().create(body=file_metadata, fields='id').execute()
        print(f"Carpeta creada: {folder_name}, ID: {file.get('id')}")
        return file.get('id')
    except Exception as e:
        print(f"Error al crear la carpeta {folder_name}: {str(e)}")
        return None

def upload_file_to_drive(folder_id, file_path):
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, mimetype='application/json')
    try:
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"Archivo subido: {file_path}, ID: {file.get('id')}")
    except Exception as e:
        print(f"Error al subir el archivo {file_path}: {str(e)}")

# Usar la función con el ID de la carpeta padre
parent_folder_id = '1K0FS2UpT51wdEmHk3zw279RdgQzdTadk'  # Reemplaza esto con el ID de tu carpeta en Google Drive

for row in datos_hoja_calculo:
    nombre_asegurado = row['Nombre Completo']
    rut = row['Rut (sin puntos ni guion)']
    marca = row['Marca Vehículo']
    modelo = row['Modelo Vehículo']
    anio = row['Año Vehículo']
    patente = row['Patente Vehículo (dejar en blanco si aun no cuenta con patente)']
    uso_vehiculo = row['Uso del Vehículo']
    estado_vehiculo = row['Estado del Vehículo']
    comuna = row['Comuna']

    if nombre_asegurado.strip():
        # Crear la carpeta en Google Drive
        folder_id = create_folder_in_drive(nombre_asegurado, parent_id=parent_folder_id)
        if not folder_id:
            print(f"Error al crear o encontrar la carpeta para {nombre_asegurado}.")
            continue

        data = {
            "marca": marca,
            "modelo": modelo,
            "anio": anio,
            "nombre_asegurado": nombre_asegurado,
            "rut": rut,
            "patente": patente,
            "uso_vehiculo": uso_vehiculo,
            "estado_vehiculo": estado_vehiculo,
            "comuna": comuna
        }

        temp_file = os.path.join(os.getcwd(), f"{nombre_asegurado}_data.json")
        with open(temp_file, "w") as f:
            json.dump(data, f)
            print(f"Datos guardados en {temp_file}: {data}")  # Confirmar que se ha guardado

        # Ejecutar scripts secuenciales
        def run_script(script_name, temp_file):
            try:
                result = subprocess.run(["python", script_name, temp_file], capture_output=True, text=True, check=True)
                nombre_archivo = result.stdout.strip()  # Obtener el nombre del archivo desde la salida estándar

                if nombre_archivo:
                    # Añadir la extensión .pdf al nombre del archivo
                    file_name = f"{nombre_archivo}.pdf"

                    # Ruta del archivo de origen y destino
                    file_path_src = os.path.join(ruta_descarga, file_name)

                    # Verificar si el archivo existe y subirlo a Google Drive
                    if os.path.exists(file_path_src):
                        upload_file_to_drive(folder_id, file_path_src)  # Sube el archivo PDF a la carpeta en Google Drive
                        print(f"Archivo {file_name} guardado correctamente en Google Drive.")
                        return True
                    else:
                        print(f"Error: Archivo {file_name} no encontrado.")
                        return False
                else:
                    print(f"Error: No se encontró el nombre del archivo en la salida de {script_name}.")
                    return False
            except subprocess.CalledProcessError as e:
                print(f"Error ejecutando {script_name}: {str(e)}")
                return False

        # Ejecutar scripts secuenciales
        if run_script("BCI_v1.py", temp_file):
            # if run_script("renta_v4.py"):
            # run_script("Mapfre_v1.py")
            print("Todos los scripts se ejecutaron correctamente y los archivos PDF se descargaron en la carpeta del asegurado.")
    else:
        print('Nombre asegurado vacío, no se crea carpeta.')
