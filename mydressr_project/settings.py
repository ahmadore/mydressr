from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-mydressr-demo-key-change-in-production'
DEBUG = True

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'tryon',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mydressr_project.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.request',
        ],
    },
}]

WSGI_APPLICATION = 'mydressr_project.wsgi.application'

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# HuggingFace Space endpoints
# CatVTON space (lightweight, fast) — primary
CATVTON_SPACE = "zhengchong/CatVTON"
# IDM-VTON space — fallback / higher quality
IDMVTON_SPACE = "yisol/IDM-VTON"

# Allow the Hugging Face frame embedding
X_FRAME_OPTIONS = "ALLOW-FROM https://huggingface.co/"

# Ensure your allowed hosts can handle Hugging Face domains
ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".hf.space", "huggingface.co"]

# Optional: CSRF trusted origins for form submissions
CSRF_TRUSTED_ORIGINS = ["https://*.hf.space"]
