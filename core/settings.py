import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-chave-temporaria-tio-tony-2026')

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',  # Deve vir ANTES do staticfiles
    'django.contrib.staticfiles',
    'cloudinary',          # Deve vir APÓS o staticfiles
    'corsheaders',
    'rest_framework',
    'loja',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi'

# Banco de dados Neon.tech via DATABASE_URL
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', ''),
        conn_max_age=600,
        ssl_require=True
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# CORRIGIDO: Colchete fechado corretamente
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'loja', 'static'),
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True

# Credenciais Mercado Pago
MERCADOPAGO_ACCESS_TOKEN = os.environ.get('MERCADOPAGO_ACCESS_TOKEN', '')

# Configuração Integrada do Cloudinary Storage
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', ''),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY', ''),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET', ''),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Configuração do WhiteNoise para produção
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Personalização Visual do Jazzmin (Admin Açaí do Tio Tony)
JAZZMIN_SETTINGS = {
    "site_title": "Painel Tio Tony",
    "site_header": "Açaí do Tio Tony",
    "site_brand": "Açaí do Tio Tony",
    "welcome_sign": "Bem-vindo ao Gestor de Pedidos e Produtos",
    "copyright": "Açaí do Tio Tony Ltd",
    "search_model": ["loja.produto"],
    "topmenu_links": [
        {"name": "Ver Site", "url": "https://acai-tio-tony-frontend.vercel.app", "new_window": True},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "auth": "fas fontawesome-user",
        "auth.user": "fas fontawesome-user",
        "loja.categoria": "fas fontawesome-list",
        "loja.produto": "fas fontawesome-wine-glass-alt",
        "loja.grupoopcao": "fas fontawesome-plus-circle",
        "loja.itemadicional": "fas fontawesome-cookie-bite",
        "loja.pedido": "fas fontawesome-shopping-cart",
    },
    "default_icon_parents": "fas fontawesome-folder",
    "default_icon_children": "fas fontawesome-circle",
    "custom_css": "admin/css/responsive_admin.css",
    "custom_js": "admin/js/toggle_excedentes.js",
}

JAZZMIN_UI_TWEAKS = {
    "theme": "pulse",                  # Tema base suave em tons de lilás/roxo claro
    "dark_mode_theme": None,
    "navbar": "navbar-dark bg-indigo",  # Barra superior em roxo açaí
    "navbar_small_text": False,
    "sidebar": "sidebar-light-indigo", # Menu lateral em fundo claro com destaques roxos
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "accent": "accent-warning",        # Detalhes em tom Dourado/Âmbar
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}
