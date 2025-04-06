FROM python:3.10-slim

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    curl \
    tar \
    && rm -rf /var/lib/apt/lists/*

# Descargar y extraer uv (release oficial desde GitHub)
RUN curl -sSL https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-unknown-linux-gnu.tar.gz -o uv.tar.gz \
    && tar -xzf uv.tar.gz \
    && mv uv-x86_64-unknown-linux-gnu/uv /usr/local/bin/uv \
    && chmod +x /usr/local/bin/uv \
    && rm -rf uv.tar.gz uv-x86_64-unknown-linux-gnu

# Crear directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto
COPY . .

# Instalar las dependencias del proyecto usando uv
RUN uv pip install --system --no-cache-dir .

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar tu app
cmd ["uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8000"]
