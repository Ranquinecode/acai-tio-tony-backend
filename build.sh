#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Gera o arquivo de migração se houver alterações no models.py
python manage.py makemigrations

# Aplica as migrações no banco Neon.tech
python manage.py migrate

# Coleta os arquivos estáticos sem conflito
python manage.py collectstatic --no-input
