#!/usr/bin/env bash
set -o errexit  # Salir si un comando falla
set -o nounset  # Error si se usa una variable no definida
set -o pipefail # Falla si un comando en un pipe falla

echo "=== Instalando dependencias del sistema ==="
# Dependencias de WeasyPrint
apt-get update && apt-get install -y --no-install-recommends \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libffi-dev \
    libgdk-pixbuf2.0-0 \
    shared-mime-info \
    fonts-dejavu-core \
    fonts-freefont-ttf \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

echo "=== Instalando dependencias de Python ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== Aplicando migraciones de Django ==="
python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "=== Listo para iniciar la app ==="