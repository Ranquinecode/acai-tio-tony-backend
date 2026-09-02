#!/usr/bin/env bash
set -o errexit

echo "📦 Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🧹 Limpando arquivos estáticos antigos..."
rm -rf staticfiles

echo "🗄️ Sincronizando o estado das migrações com o Neon.tech..."
# Marca a migração 0005 como concluída no banco sem tentar re-criar a tabela
python manage.py migrate loja 0005 --fake

# Garante que todo o resto esteja atualizado
python manage.py migrate --noinput

echo "🎨 Coletando arquivos estáticos..."
python manage.py collectstatic --no-input

echo "✅ Build concluído com sucesso!"
