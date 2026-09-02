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

# Banco de dados Neon.tech via DATABASE_URL com fallback para SQLite local
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

# Garante a busca dos arquivos estáticos na pasta de cada APP (ex: loja/static)
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
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

# Padrão Moderno de Storages do Django 4.2+
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.StaticFilesStorage",
    },
}

# Personalização Visual do Jazzmin (Admin Moderno - Thony Snacks / Açaí do Tio Tony)
JAZZMIN_SETTINGS = {
    "site_title": "Painel Thony Snacks",
    "site_header": "Gestão Thony Snacks",
    "site_brand": "Thony Snacks",
    "welcome_sign": "Painel de Controle e Gestão do Cardápio",
    "copyright": "Thony Snacks",
    "search_model": ["loja.produto", "loja.pedido"],
    "topmenu_links": [
        {"name": "Ver Loja Online 🚀", "url": "https://acai-tio-tony-frontend.vercel.app", "new_window": True},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user-shield",
        "auth.group": "fas fa-users",
        "loja.pedido": "fas fa-shopping-bag",
        "loja.produto": "fas fa-ice-cream",
        "loja.categoria": "fas fa-tags",
        "loja.grupoopcao": "fas fa-layer-group",
        "loja.itemadicional": "fas fa-plus-circle",
        "loja.itemgrupoopcao": "fas fa-link",
        "loja.itemcombo": "fas fa-boxes",
    },
    "order_with_respect_to": [
        "loja.pedido",
        "loja.produto",
        "loja.categoria",
        "loja.grupoopcao",
        "loja.itemadicional",
        "auth",
    ],
    "default_icon_parents": "fas fa-folder",
    "default_icon_children": "fas fa-circle",
    
    # Caminhos para loja/static/loja/css e loja/static/loja/js
    "custom_css": "loja/css/admin_custom.css",
    "custom_js": "loja/js/admin_custom.js",
    
    "use_google_fonts_cdn": True,
    "changeform_format": "single",
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-warning",
    "navbar": "navbar-dark bg-dark",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-warning",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "flatly",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}
