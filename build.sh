#!/usr/bin/env bash
# Interrompe a execução imediatamente se qualquer comando falhar
set -o errexit

echo "📦 Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🧹 Limpando arquivos estáticos antigos..."
rm -rf staticfiles

echo "📝 Gerando migrações para alterações nos models..."
python manage.py makemigrations loja --noinput

echo "🗄️ Aplicando migrações no banco Neon.tech..."
python manage.py migrate --noinput

echo "🎨 Coletando arquivos estáticos..."
python manage.py collectstatic --no-input

echo "✅ Build concluído com sucesso!"
