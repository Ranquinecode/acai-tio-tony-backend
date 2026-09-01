import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get('ADMIN_USERNAME', 'admin')
email = os.environ.get('ADMIN_EMAIL', 'admin@acaidotiotony.com')
password = os.environ.get('ADMIN_PASSWORD', 'TioTony@2026')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superusuario '{username}' criado com sucesso!")
else:
    print(f"Superusuario '{username}' ja existe.")
