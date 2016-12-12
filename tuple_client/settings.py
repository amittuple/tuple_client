"""
Django settings for tuple_client project.

Generated by 'django-admin startproject' using Django 1.10.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'hk*3m=tp10@brjhq825y3_^c0e(jdn*w+_ksa7akck3erix(7#'
SECRET_KEY = 'od1!uqzw&v3%rgivpo%i2-@7#r@!4$9haqt)ylgt*e-a+uwz72'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
#
# SESSION_COOKIE_HTTPONLY = True
#
# SESSION_COOKIE_DOMAIN = 'localhost'



# Application definition

INSTALLED_APPS = [
    'login',
    'user_profile',
    'mapper',
    'connect_client_db',
    'database_management',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # CELERY
    'django_celery_results',
    # chatbot here
    'team',
    'banana_py',
    'rest_framework',
    'build_mailchimp',
    # slack coading here
    'slack_bot',
]


# MIDDLEWARE_CLASSES = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tuple_client.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'tuple_client.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres_db',
        'HOST': 'localhost',
        'PORT': '5432',
        'USER': 'postgres_user',
        'PASSWORD': 'admin'
    },
    'common': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tuple_common_db',
        'HOST': 'tuple-common-server-db.c3yxphqgag3s.ap-southeast-1.rds.amazonaws.com',
        'PORT': '5432',
        'USER': 'tuplecommon1',
        'PASSWORD': 'tuple-common-db'
    }
}

# DATABASE_ROUTERS = ['tuple_client.routers.AuthRouter', 'tuple_client.routers.ClientDbRouter']
DATABASE_ROUTERS = ['tuple_client.routers.OtherRouter', 'tuple_client.routers.DefaultRouter']

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

CELERY_RESULT_BACKEND = 'django-db'

MAILCHIMP_CLIENT_ID = '301551589835'
MAILCHIMP_CLIENT_SECRET = '07a893f0cbb38592b226e95a4f490ad0'
MAILCHIMP_REDIRECT_URI = 'http://127.0.0.1:8000/bananas/ripe/'
MAILCHIMP_COMPLETE_URI = 'http://127.0.0.1:8000/build-mailchimp/complete/'


# CELERY DATABASE
CELERY_RESULT_BACKEND = 'django-db'
#  slack key and secrate key

CLIENT_ID = "14632386742.108610646339"
CLIENT_SECRET = "c5b02a54bd14ef5fc528e91536fc5c21"
