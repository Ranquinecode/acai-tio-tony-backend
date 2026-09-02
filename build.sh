#!/usr/bin/env bash
set -o errexit

echo "📦 Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🧹 Limpando arquivos estáticos antigos..."
rm -rf staticfiles

echo "📝 Forçando a criação das migrações do App loja..."
python manage.py makemigrations loja --noinput

echo "🗄️ Aplicando migrações no banco Neon.tech..."
python manage.py migrate loja --noinput
python manage.py migrate --noinput

echo "🎨 Coletando arquivos estáticos..."
python manage.py collectstatic --no-input

echo "✅ Build concluído!"
