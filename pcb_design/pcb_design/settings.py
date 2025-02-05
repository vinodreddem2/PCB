"""
Django settings for pcb_design project.

Generated by 'django-admin startproject' using Django 4.2.17.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from datetime import timedelta 
import os 
from dotenv import load_dotenv
import dj_database_url
load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-jawafdzu&qb#a(n#udlvf*9_oqv$o%_=znvu9v#pp6kri=2(2o'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True
ALLOWED_HOSTS = ['pcb-design-5nqf.onrender.com','127.0.0.1', '*']

# ALLOWED_HOSTS = ["127.0.0.1","localhost"]
# ALLOWED_HOSTS+=os.getenv("ALLOWED_HOSTS", "").split(",")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'import_export',
    'drf_yasg',   
    'right_to_draw',
    'authentication',
    'masters',
    "corsheaders",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'middleware.current_user_middleware.CurrentUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGIN_REGEXES = [r"^https?://localhost(:\d+)?$"]
ROOT_URLCONF = 'pcb_design.urls'

AUTH_USER_MODEL= 'authentication.CustomUser'

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

WSGI_APPLICATION = 'pcb_design.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default':dj_database_url.parse(os.getenv('DATABASE_URL')) 
# }

# # Ensure SSL is enabled (no SSL root certificate required)
# DATABASES['default']['OPTIONS'] = {
#     'sslmode': 'require',  # Ensure the connection is over SSL
# }

# DATABASES = {}

# DATABASE_URL = os.getenv("DATABASE_URL", "")
# if DATABASE_URL:
#     DATABASES['default'] = dj_database_url.parse(DATABASE_URL, conn_max_age=600, ssl_require=False)

# Parse the database URL from the environment variable
# DATABASES = {
#     'default': dj_database_url.parse(os.getenv('DATABASE_URL'), conn_max_age=600)
# }

# Set SSL connection mode to 'require'
# DATABASES['default']['OPTIONS'] = {
#     'sslmode': 'require',  # Enforces SSL connection, no root cert required
# }

# https://www.dundas.com/support/learning/documentation/installation/how-to-enable-sql-server-authentication#:~:text=In%20the%20Object%20Explorer%2C%20right,the%20server%20and%20click%20Properties.&text=On%20the%20Security%20page%20under,mode%20and%20then%20click%20OK.&text=In%20the%20Object%20Explorer%2C%20right%2Dclick%20your%20server%20and%20click,it%20must%20also%20be%20restarted.

DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': os.getenv('DB_NAME', 'PCB'),
        'USER': os.getenv('DB_USER', 'admin'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'Server.2'),
        'HOST': os.getenv('DB_HOST', 'localhost\SQLEXPRESS'),
        'PORT': '',
        'OPTIONS': {
            'autocommit': True,
            'driver': 'ODBC Driver 17 for SQL Server',
            'extra_params': 'DataTypeCompatibility=80;MARS Connection=True;',
            'use_legacy_date_fields': True,
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'authentication.custom_authentication.CustomJWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'authentication.custom_permissions.IsAuthorized',  # Default permission class
    ),
}

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
APPEND_SLASH=False

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=150),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}