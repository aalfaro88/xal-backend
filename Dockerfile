# Usar una imagen base de Python
FROM python:3.8-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos del proyecto al contenedor
COPY . /app

# Instalar las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto en el que la aplicación estará escuchando
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "./app/main.py"]