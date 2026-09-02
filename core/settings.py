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

# Banco de dados Neon.tech via DATABASE_URL com fallback para SQLite local se não houver variável
DATABASE_URL_ENV = os.environ.get('DATABASE_URL')

if DATABASE_URL_ENV:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL_ENV,
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
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
STATICFILES_DIRS = []

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

# Padrão Moderno de Storages do Django 4.2+
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.StaticFilesStorage",
    },
}

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
        "auth": "fas fa-users",
        "auth.user": "fas fa-user",
        "loja.categoria": "fas fa-list",
        "loja.produto": "fas fa-wine-glass-alt",
        "loja.grupoopcao": "fas fa-plus-circle",
        "loja.itemadicional": "fas fa-cookie-bite",
        "loja.itemcombo": "fas fa-cubes",
        "loja.pedido": "fas fa-shopping-cart",
    },
    "default_icon_parents": "fas fa-folder",
    "default_icon_children": "fas fa-circle",
    "custom_css": "loja/css/custom_admin.css",
    "custom_js": "loja/js/custom_admin.js",
}

JAZZMIN_UI_TWEAKS = {
    "theme": "pulse",
    "dark_mode_theme": None,
    "navbar": "navbar-dark bg-indigo",
    "navbar_small_text": False,
    "sidebar": "sidebar-light-indigo",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "accent": "accent-warning",
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}
