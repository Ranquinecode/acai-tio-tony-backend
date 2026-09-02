#!/usr/bin/env bash
set -o errexit

echo "📦 Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🧹 Limpando arquivos estáticos antigos..."
rm -rf staticfiles

echo "📝 Gerando migrações pendentes..."
python manage.py makemigrations loja --noinput

echo "🗄️ Aplicando migrações no banco Neon.tech..."
# --fake-initial diz ao Django: se a tabela/coluna já existir no Postgres, não tente recriá-la, apenas marque como aplicada!
python manage.py migrate --fake-initial --noinput

echo "🎨 Coletando arquivos estáticos..."
python manage.py collectstatic --no-input

echo "✅ Build concluído com sucesso!"
