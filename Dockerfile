FROM python:3.12-slim

# Establecer el directorio de trabajo
WORKDIR /project

# Copiar los archivos de requisitos
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el contenido del proyecto
COPY . .

# Exponer el puerto
EXPOSE 8000

# Comando por defecto (ejecutar la API)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]