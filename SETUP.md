# 🔧 Guía de Configuración para Desarrolladores

## Requisitos del Sistema

- Python 3.8 o superior
- pip (se instala con Python)
- ChromeDriver compatible con tu versión de Chrome
- Git

### Verificar Python

```bash
python --version
# Debe mostrar Python 3.8.x o superior
```

## Instalación Paso a Paso

### 1. Clonar Repositorio

```bash
git clone https://github.com/usuario/GPTSeguros.git
cd GPTSeguros
```

### 2. Crear Entorno Virtual

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**En macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Verificar que esté activado (debe mostrar `(venv)` en el prompt):
```bash
which python  # En Linux/Mac
# o
where python  # En Windows
```

### 3. Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Para desarrollo con herramientas adicionales:
```bash
pip install -r requirements-dev.txt  # Si existe
```

### 4. Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar con tu editor favorito
# Windows (Notepad)
notepad .env

# macOS/Linux (Nano)
nano .env

# VS Code
code .env
```

Editar el archivo `.env` con tus credenciales reales:
```env
DJANGO_SECRET_KEY=tu_clave_secreta_aqui
DEBUG=True

# Credenciales que tengas disponibles
BCI_USUARIO=tu_usuario
BCI_CONTRASENA=tu_password
# ... etc
```

### 5. Instalar ChromeDriver

**Opción A: Automático (recomendado)**

```bash
pip install webdriver-manager
```

En el código:
```python
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
```

**Opción B: Manual**

1. Descargar desde: https://chromedriver.chromium.org/
2. Colocar en `C:\Windows\System32` (Windows) o `/usr/local/bin` (Mac/Linux)

Verificar:
```bash
chromedriver --version
```

### 6. Inicializar Django

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario (opcional)
python manage.py createsuperuser
```

### 7. Verificar Instalación

```bash
# Test rápido
python -c "import selenium; print(f'Selenium {selenium.__version__} OK')"
python -c "import django; print(f'Django {django.__version__} OK')"

# Test de configuración
python -c "from selenium_gpt.config import BCI_USUARIO; print('Config OK')"
```

## Uso del Proyecto

### CLI - Cotizador por Consola

```bash
python cotizador.py
```

Seleccionar opción y seguir instrucciones.

### GUI - Interfaz Gráfica (Tkinter)

```bash
python selenium_gpt/front_v2.py
```

### Django Server

```bash
python manage.py runserver
# Acceder a http://localhost:8000
```

### API REST (Django REST Framework)

La API está lista en `http://localhost:8000/api/`

## Jupyter Notebooks

Para ejecutar los notebooks de prueba:

```bash
pip install jupyter
jupyter notebook
```

Ir a `request/request.ipynb`

## Solución de Problemas Comunes

### "ModuleNotFoundError: No module named 'selenium'"

```bash
# Asegurarte que el venv esté activado
# En Windows
venv\Scripts\activate

# Volver a instalar
pip install selenium
```

### "chromedriver not found"

```bash
# Opción 1: Instalar webdriver-manager
pip install webdriver-manager

# Opción 2: Descargar manualmente
# https://chromedriver.chromium.org/ → descargar versión compatible
# Guardar en carpeta del proyecto o en PATH
```

### ".env not found"

```bash
# Crear desde ejemplo
cp .env.example .env

# Editar y agregar credenciales
nano .env
```

### "Port 8000 already in use" (Django)

```bash
# Usar otro puerto
python manage.py runserver 8001

# O encontrar proceso en puerto 8000
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000
```

### "Permission denied" (ejecutables)

```bash
# En Linux/Mac
chmod +x chromedriver
chmod +x selenium_gpt/front_v2.py
```

## Estructura de Trabajo Recomendada

```
Mi_Workspace/
├── GPTSeguros/          # Este repositorio
│   ├── .env             # Local, no comitear
│   ├── venv/            # Virtual environment
│   ├── db.sqlite3       # Base de datos local
│   └── cotizacion/      # PDFs descargados
│
└── Documentación/       # Tus notas personales
```

## Prácticas Recomendadas

### 1. Antes de Comitear

```bash
# Verificar cambios
git status

# Revisar cambios antes de agregar
git diff

# NO agregar archivos sensibles
git add -u  # Solo tracking changed files
git add archivo_especifico.py

# Nunca hagas
git add .env        # ❌ NUNCA
git add .env.*      # ❌ NUNCA
git add db.sqlite3  # ❌ NUNCA (si tiene datos)
```

### 2. Mantener Dependencias Actualizadas

```bash
# Ver qué está desactualizado
pip list --outdated

# Actualizar específico
pip install --upgrade selenium

# Actualizar todo
pip install -U -r requirements.txt

# Exportar dependencias actualizadas
pip freeze > requirements.txt
```

### 3. Logs y Debugging

```python
# En tu código
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Iniciando sesión...")
logger.error("Error en login")
```

### 4. Tests y Validación

```bash
# Si existen tests
python manage.py test

# Linting
pip install pylint
pylint selenium_gpt/

# Formateo de código
pip install black
black selenium_gpt/
```

## Entornos Recomendados por Caso de Uso

### Para Aprender

- Editor: VS Code
- Adicionales: Jupyter, IPython
- Base de datos: SQLite (por defecto)

### Para Desarrollo de Características

- Editor: VS Code / PyCharm
- Herramientas: Git, Pylint, Black
- Base de datos: SQLite primero, PostgreSQL en producción

### Para Testing/QA

- Ambiente separado de Dev
- Credenciales de aseguradoras de prueba
- Logs detallados activados

## Desactivar Entorno Virtual

Cuando termines de trabajar:

```bash
deactivate
```

## Proximos Pasos

Después de configurar:

1. Lee [README.md](README.md) para entender el proyecto
2. Lee [SECURITY.md](SECURITY.md) para prácticas de seguridad
3. Explora `selenium_gpt/` para entender la arquitectura
4. Revisa `quoterapp/` para la parte Django

## Soporte

- 📖 Documentación: Ver archivos `.md` en raíz
- 🐛 Bugs: Abrir issue en GitHub
- 💬 Preguntas: Discusiones en GitHub

---

**Última actualización**: Abril 2026
