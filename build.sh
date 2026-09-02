#!/usr/bin/env bash
set -o errexit

echo "📦 Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🧹 Limpando arquivos estáticos antigos..."
rm -rf staticfiles

echo "📝 Gerando arquivos de migração limpos..."
python manage.py makemigrations loja --noinput

echo "🗄️ Aplicando migrações com fake-initial..."
python manage.py migrate --fake-initial --noinput

echo "👤 Criando superusuário admin (se não existir)..."
python -c "import os, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings'); django.setup(); from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@email.com', 'Admin123456')"

echo "🎨 Coletando arquivos estáticos..."
python manage.py collectstatic --no-input

echo "✅ Build concluído com sucesso!"
