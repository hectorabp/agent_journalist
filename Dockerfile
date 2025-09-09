# Usar una imagen base de Python
FROM python:3.11.9

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Instalar el paquete de locales
RUN apt-get update && apt-get install -y locales

# Generar los locales necesarios
RUN locale-gen es_ES.UTF-8

# Instalar las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Establecer PYTHONUNBUFFERED para desactivar el búfer
ENV PYTHONUNBUFFERED=1

# Copiar el código fuente del sistema
COPY controller /app/controller
COPY modules /app/modules
COPY routes /app/routes
COPY notas /app/notas
COPY static /app/static
COPY templates /app/templates
COPY app.py .

# Configurar la localización en el sistema operativo del contenedor
ENV LC_ALL es_ES.UTF-8
ENV LANG es_ES.UTF-8

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
