# Dockerfile
FROM python:3.11.9-slim

ENV PYTHONUNBUFFERED 1

# Instala dependencias del sistema
RUN apt-get update && \
    apt-get install -yq --no-install-recommends \
    libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 \
    libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 \
    libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 \
    libx11-6 libx11-xcb1 libxcb1 libxcursor1 libxdamage1 libxext6 libxfixes3 \
    libxi6 libxrandr2 libxrender1 libxss1 libxtst6 libnss3 \
    && rm -rf /var/lib/apt/lists/*

# Copia el código al contenedor
COPY . /gptseguros
WORKDIR /gptseguros

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Crear y cambiar a un usuario no root
RUN adduser --disabled-password celeryuser
USER celeryuser

# Expone el puerto para Django
EXPOSE 8000

# Comando por defecto para iniciar Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
