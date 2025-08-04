#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail

echo "=== Inicio del despliegue ==="

# 1. Instalar dependencias nativas si apt-get está disponible
if command -v apt-get >/dev/null 2>&1; then
  echo "🔧 Instalando dependencias del sistema para WeasyPrint y Poppler..."
  apt-get update
  apt-get install -y \
    libpango-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    fonts-dejavu-core \
    poppler-utils
else
  echo "⚠️  apt-get no está disponible; asumo que las dependencias nativas ya están presentes."
fi

# 2. Verificar que pdftoppm (Poppler) esté accesible
if ! command -v pdftoppm >/dev/null 2>&1; then
  echo "⚠️  pdftoppm no se encontró en PATH. La conversión a PNG fallará sin Poppler."
else
  echo "✅ pdftoppm detectado:" 
  pdftoppm -v || true
fi

# 3. Actualizar pip e instalar requirements
echo "📦 Actualizando pip e instalando dependencias Python..."
python -m pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

# 4. Collectstatic (Django)
echo "📁 Ejecutando collectstatic..."
python manage.py collectstatic --noinput

# 5. Migraciones
echo "🗃️ Aplicando migraciones..."
python manage.py makemigrations
python manage.py migrate

echo "✅ Despliegue completado."
