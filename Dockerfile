# Imagen base fijada por versión: nunca :latest, porque "latest" cambia con el tiempo
# y deja de ser reproducible. slim reduce el tamaño sin perder el intérprete completo.
FROM python:3.13-slim

# Sin archivos .pyc y con salida sin búfer: los logs aparecen en orden en docker logs.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Las dependencias se copian e instalan ANTES del código: así Docker reutiliza
# la capa de instalación mientras requirements.txt no cambie, y el build es rápido.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Solo el método entra en la imagen. Los datos NO: se montan como volumen.
# (Regla 4 de Nüst et al., 2020: la imagen contiene el procedimiento, no la información.)
COPY src/ ./src/
COPY perfilamiento_agua.ipynb ./

CMD ["python", "src/perfilamiento_agua.py"]
