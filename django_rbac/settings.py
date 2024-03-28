import pymysql
import os
from dotenv import load_dotenv
load_dotenv()
pymysql.install_as_MySQLdb()

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'auth_app',
    'policy_app',
    'service_app'
]

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django_rbac.middleware.SecurityMiddleware'
]

ROOT_URLCONF = 'django_rbac.urls'

TEMPLATES = []

WSGI_APPLICATION = 'django_rbac.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD')
    },
}

AUTH_PASSWORD_VALIDATORS = []


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


JWT_TOKEN_TIME = os.getenv('JWT_ACCESS_TOKEN_EXPIRES')
JWT_REFRESH_TIME = os.getenv('JWT_REFRESH_TOKEN_EXPIRES')
JWT_ALGO = os.getenv('JWT_ALGO')
JWT_SECRET = os.getenv('APP_JWT_SECRET')

