# 🛡️ GPTSeguros — Cotizador Automatizado de Seguros

Sistema de automatización para la obtención de cotizaciones de seguros de vehículos en múltiples aseguradoras chilenas mediante web scraping con Selenium y un backend Django.

Desarrollado como proyecto personal para reducir el tiempo operativo de corredores de seguros al cotizar en múltiples plataformas simultáneamente.

---

## ¿Qué hace este proyecto?

- 🤖 Automatiza el ingreso de datos y descarga de cotizaciones en portales de aseguradoras
- 📄 Descarga automáticamente los PDFs con las cotizaciones generadas
- 🖥️ Ofrece interfaz gráfica (Tkinter) para uso sin línea de comandos
- 🌐 Incluye backend Django con API REST para integración web
- 🔐 Gestiona credenciales de forma segura mediante variables de entorno

---

## Aseguradoras soportadas

| Aseguradora | Estado |
|---|---|
| BCI Seguros | ✅ Funcional |
| Renta Nacional | ✅ Funcional |
| FID Seguros | ✅ Funcional |
| Sura | ✅ Funcional |
| Mapfre | ⚠️ Limitaciones anti-automatización |
| HDI | ⚠️ Limitaciones anti-automatización |
| ANS | ❌ Descontinuado |
| Real Chile | ⏳ En desarrollo |

---

## Impacto real

| Resultado | Detalle |
|---|---|
| Reducción de tiempo operativo | Cotización simultánea en múltiples portales sin intervención manual |
| Cobertura | 4 aseguradoras funcionales, 2 en investigación |
| Formatos de salida | PDF descargado y renombrado automáticamente por cliente |
| Modos de uso | CLI, interfaz gráfica y API REST |

---

## 🛠️ Stack

| Área | Librerias |
|---|---|
| **Automatización** | Python, Selenium, ChromeDriver |
| **Backend** | Django, Django REST Framework |
| **Interfaz gráfica** | Tkinter |
| **Configuración** | python-dotenv |
| **Base de datos** | SQLite (desarrollo) |

---

## 📁 Estructura del proyecto

```
GPTSeguros/
│
├── gptproyect/              # Configuración Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── quoterapp/               # Aplicación Django principal
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── templates/
│
├── selenium_gpt/            # Módulo de automatización por aseguradora
│   ├── config.py            # Configuración centralizada
│   ├── cotizar.py
│   ├── front_v2.py          # Interfaz gráfica (Tkinter)
│   ├── bci/                 # Cotizador BCI
│   ├── sura/                # Cotizador Sura
│   ├── fid/                 # Cotizador FID
│   ├── renta/               # Cotizador Renta Nacional
│   ├── mapfre/              # Cotizador Mapfre
│   ├── hdi/                 # Cotizador HDI
│   └── ans/                 # Cotizador ANS (descontinuado)
│
├── utils/                   # Utilidades generales
├── request/                 # Notebooks de prueba
├── cotizador.py             # Script CLI principal
├── manage.py
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## 🚀 Instalación y configuración

### Requisitos previos
- Python 3.8+
- ChromeDriver compatible con tu versión de Chrome
- pip

### Pasos

1. **Clonar el repositorio**
```bash
git clone https://github.com/OscarPainen/GPTSeguros.git
cd GPTSeguros
```

2. **Crear entorno virtual**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus credenciales de cada aseguradora
```

5. **Inicializar base de datos**
```bash
python manage.py migrate
```

---

## ⚙️ Variables de entorno

El archivo `.env.example` incluye todas las variables necesarias:

```env
# Django
DJANGO_SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# Credenciales por aseguradora
BCI_USUARIO=your_user
BCI_CONTRASENA=your_password
SURA_USUARIO=your_user
SURA_CONTRASENA=your_password
# ... (una entrada por aseguradora)

# Configuración de descargas
DOWNLOAD_PATH=./cotizacion
```

---

## 🎮 Modos de uso

### CLI (línea de comandos)
```bash
python cotizador.py
```

### Interfaz gráfica (Tkinter)
```bash
python selenium_gpt/front_v2.py
```

### Backend Django
```bash
python manage.py runserver
```
Accede en `http://localhost:8000`

---

## 📋 Datos requeridos para cotizar

| Campo | Ejemplo |
|---|---|
| RUT del asegurado | 12.345.678-9 |
| Marca del vehículo | Honda |
| Modelo | Civic |
| Año | 2000 |
| Nombre del asegurado | Peter Parker |

---

## 🐛 Limitaciones conocidas

| Problema | Aseguradora | Estado |
|---|---|---|
| Reconocimiento de ciertos modelos | BCI | En investigación |
| Reconocimiento de marcas | Sura | En investigación |
| Protección anti-automatización | Mapfre, HDI | Limitación técnica del sitio |
| Tiempos de respuesta variables | General | En optimización |

---

## 🔒 Seguridad

- Credenciales gestionadas exclusivamente mediante variables de entorno
- `.env` excluido del repositorio vía `.gitignore`
- `DJANGO_SECRET_KEY` configurable por entorno
- `DEBUG=False` recomendado en producción

---

## ⚖️ Aviso

Este proyecto es una herramienta de desarrollo personal. El uso de automatización web debe respetar los términos de servicio de cada plataforma. El autor no se responsabiliza por el uso indebido de esta herramienta.

---

## Autor

**Oscar Andrés Painen Briones**  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Oscar%20Painen-blue?logo=linkedin)](https://www.linkedin.com/in/oscarpainenbriones/)

---

*Desarrollado con Python, Django y Selenium.*