#!/usr/bin/env bash
set -o errexit

echo "📦 Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🧹 Limpando arquivos estáticos antigos..."
rm -rf staticfiles

echo "🔧 Sincronizando colunas no PostgreSQL (Neon.tech)..."
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
from django.db import connection

queries = [
    'ALTER TABLE loja_grupoopcao ADD COLUMN IF NOT EXISTS cobrar_camada_extra BOOLEAN DEFAULT FALSE;',
    'ALTER TABLE loja_itemadicional ADD COLUMN IF NOT EXISTS disponibilidade VARCHAR(20) DEFAULT \'disponivel\';',
    'ALTER TABLE loja_produto ADD COLUMN IF NOT EXISTS preco_camada_extra NUMERIC(6, 2) DEFAULT 2.00;',
    'ALTER TABLE loja_produto ADD COLUMN IF NOT EXISTS eh_customizavel BOOLEAN DEFAULT TRUE;',
    'ALTER TABLE loja_produto ADD COLUMN IF NOT EXISTS eh_combo BOOLEAN DEFAULT FALSE;'
]

with connection.cursor() as cursor:
    for q in queries:
        try:
            cursor.execute(q)
        except Exception as e:
            print(f'Aviso SQL: {e}')
"

echo "📝 Gerando arquivos de migração para o app loja..."
python manage.py makemigrations loja --noinput

echo "🗄️ Aplicando migrações no banco..."
python manage.py migrate --fake-initial --noinput

echo "👤 Criando superusuário admin (se não existir)..."
python -c "import os, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings'); django.setup(); from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@email.com', 'Admin123456')"

echo "🎨 Coletando arquivos estáticos..."
python manage.py collectstatic --no-input

echo "✅ Build concluído com sucesso!"
