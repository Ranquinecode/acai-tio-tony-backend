#!/usr/bin/env bash
set -o errexit

echo "📦 Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🧹 Limpando arquivos estáticos antigos..."
rm -rf staticfiles

echo "🗄️ Aplicando migrações (com tratamento de estado)..."
# Marca a migração problemática como aplicada (falsamente) caso ela já exista no banco
python manage.py migrate loja --fake 0004_grupoopcao_permitir_repeticao_and_more || true

# Roda o restante das migrações normalmente
python manage.py migrate --noinput

echo "🎨 Coletando arquivos estáticos..."
python manage.py collectstatic --no-input

echo "✅ Build concluído com sucesso!"
