# GPTSeguros - Automated Insurance Quote System

Sistema automatizado de cotización de seguros que obtiene cotizaciones de múltiples aseguradoras chilenas mediante web scraping con Selenium.

## 📋 Descripción del Proyecto

GPTSeguros es una herramienta que automatiza el proceso de obtención de cotizaciones de seguros de vehículos a través de web scraping. El sistema consulta múltiples aseguradoras y descarga automáticamente los PDFs con las cotizaciones.

### Características

- ✅ Cotización automatizada de seguros de vehículos
- ✅ Soporte para 8 aseguradoras diferentes
- ✅ Descarga automática de PDFs con cotizaciones
- ✅ Interfaz gráfica (Tkinter) para facilitar el uso
- ✅ Backend Django con API REST
- ✅ Configuración segura con variables de entorno

## 🏢 Aseguradoras Soportadas

| Aseguradora | Estado | URL |
|---|---|---|
| BCI Seguros | ✅ Funcional | https://oficinavirtual.bciseguros.cl/ |
| Renta Nacional | ✅ Funcional | https://sgi.rentanacional.cl/ |
| FID Seguros | ✅ Funcional | https://portal.fidseguros.cl/ |
| Sura | ✅ Funcional | https://seguros.sura.cl/ |
| Mapfre | ⚠️ Limitaciones* | https://portalcorredores.mapfre.cl/ |
| HDI | ⚠️ Limitaciones* | https://www.hdi.cl/ |
| ANS | ❌ Descontinuado | https://www.ant.cl/ |
| Real Chile | ⏳ En desarrollo | https://apps4.realechile.cl/ |

*Limitaciones técnicas debido a protecciones anti-automatización del sitio web

## 🚀 Inicio Rápido

### Requisitos Previos

- Python 3.8+
- pip (gestor de paquetes de Python)
- ChromeDriver (para Selenium)

### Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd GPTSeguros
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   
   # En Windows
   venv\Scripts\activate
   
   # En macOS/Linux
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   ```bash
   # Copiar el archivo de ejemplo
   cp .env.example .env
   
   # Editar .env con tus credenciales
   nano .env  # o tu editor preferido
   ```

5. **Crear base de datos Django**
   ```bash
   python manage.py migrate
   ```

## ⚙️ Configuración

### Variables de Entorno (.env)

El archivo `.env` debe contener las siguientes variables:

```env
# Django
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# Credenciales de Aseguradoras
BCI_USUARIO=user
BCI_CONTRASENA=password
SURA_USUARIO=user
SURA_CONTRASENA=password
# ... (una para cada aseguradora)

# Configuración General
DOWNLOAD_PATH=./cotizacion
```

**⚠️ IMPORTANTE**: Nunca comitear el archivo `.env` al repositorio. Usar `.env.example` como referencia.

## 📁 Estructura del Proyecto

```
GPTSeguros/
├── gptproyect/              # Configuración Django
│   ├── settings.py          # Configuración principal
│   ├── urls.py
│   └── wsgi.py
├── quoterapp/               # Aplicación Django principal
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── templates/
├── selenium_gpt/            # Módulo de automatización
│   ├── config.py            # Configuración centralizada
│   ├── cotizar.py
│   ├── front_v2.py          # Interfaz gráfica (Tkinter)
│   ├── ans/                 # Cotizador ANS
│   ├── bci/                 # Cotizador BCI
│   ├── sura/                # Cotizador SURA
│   ├── mapfre/              # Cotizador Mapfre
│   ├── hdi/                 # Cotizador HDI
│   ├── fid/                 # Cotizador FID
│   └── renta/               # Cotizador Renta Nacional
├── request/                 # Notebooks de prueba
│   └── request.ipynb
├── utils/                   # Utilidades generales
│   ├── front.py
│   ├── graph.py
│   └── themes.py
├── requirements.txt
├── .env.example
├── .gitignore
├── cotizador.py             # Script de consola principal
└── manage.py                # Gestor Django
```

## 🎮 Uso

### Opción 1: Interfaz de Línea de Comandos

```bash
python cotizador.py
```

Este script proporciona un menú interactivo para seleccionar la aseguradora y datos del vehículo.

### Opción 2: Interfaz Gráfica (Tkinter)

```bash
python selenium_gpt/front_v2.py
```

### Opción 3: Backend Django + API REST

```bash
python manage.py runserver
```

Luego acceder a `http://localhost:8000` o usar la API REST.

## 🔐 Seguridad

Este proyecto maneja credenciales sensibles. Se implementan las siguientes medidas:

- ✅ Credenciales en variables de entorno (`dotenv`)
- ✅ `.env` incluido en `.gitignore`
- ✅ Secret key de Django en variables de entorno
- ✅ DEBUG=False en producción
- ✅ Validación de entrada en formularios

### Mejores Prácticas

1. **Nunca** comitear archivos `.env`, `credentials.json` o archivos con datos sensibles
2. Usar `.env.example` como plantilla de configuración
3. Cambiar la `DJANGO_SECRET_KEY` en producción
4. Usar credenciales específicas/tokens para la aplicación
5. Rotar credenciales periódicamente
6. Usar HTTPS en producción

## 📊 Datos del Vehículo Requeridos

Para realizar una cotización, se necesita:

- **RUT**: Número de identificación del cliente
- **Patente**: Placa del vehículo
- **Marca**: Marca del vehículo (ej: MAZDA, Toyota)
- **Modelo**: Modelo específico (ej: CX-5, Corolla
- **Año**: Año de fabricación
- **Nombre del Asegurado**: Nombre completo

## 🐛 Problemas Conocidos

| Problema | Aseguradora | Estado |
|---|---|---|
| No reconoce ciertos modelos | BCI | En investigación |
| Problemas al reconocer marcas | Sura | En investigación |
| Tiempos de respuesta lentos | General | En optimización |
| Detecta automatización | Mapfre | Limitación técnica |
| Inestabilidad de página | HDI | Limitación técnica |

## 📈 Roadmap

- [ ] Soporte para WebDriver Playwright (alternativa a Selenium)
- [ ] Sistema de caché de cotizaciones
- [ ] Histórico de cotizaciones
- [ ] Exportación a Excel/CSV
- [ ] API público con autenticación
- [ ] Integración con Google Sheets
- [ ] Aplicación móvil
- [ ] Soporte para seguros de vida

## 🛠️ Desarrollo

### Correr tests

```bash
python manage.py test
```

### Análisis de código

```bash
python -m pylint selenium_gpt/
python -m black selenium_gpt/ --check
```

### Logs de debugging

Los logs se guardan en `logs/` con rotación diaria.

## 📝 Licencia

Especificar la licencia del proyecto aquí.

## 👥 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abrir un Pull Request

## 📧 Contacto y Soporte

Para reportar bugs o solicitar nuevas funcionalidades, abrir un issue en el repositorio.

## ⚖️ Aviso Legal

Este proyecto es una herramienta de prueba/desarrollo. El uso de web scraping debe respetar los términos de servicio de cada sitio web. Los desarrolladores no son responsables del uso indebido de esta herramienta.

---

**Última actualización**: Abril 2026
**Versión**: 2.0.0 (Reestructuración de Seguridad)

Al hacer las conexiones con la interfaz grafica hay problemas para la realizacion en orden; algunas soluciones son: boton que ejecute por modelo usando la informacion global.

*Por realizar*:
* Reale: Hay que hacerlo desde 0
* Zurich: Tiene precios atractivos

### Version 2
Traspasar la idea realizada en la V1 a una aplicacion web atraves de django. 

