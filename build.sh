#!/usr/bin/env bash
set -o errexit

echo "📦 Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🧹 Limpando arquivos estáticos antigos..."
rm -rf staticfiles

echo "💥 Resetando tabelas antigas do banco..."
python -c "from django.db import connection; cursor = connection.cursor(); cursor.execute('DROP SCHEMA public CASCADE; CREATE SCHEMA public;')"

echo "🗄️ Aplicando migração 0001_initial limpa..."
python manage.py migrate --noinput

echo "🎨 Coletando arquivos estáticos..."
python manage.py collectstatic --no-input

echo "✅ Build concluído com sucesso!"
