import os
from config.env import env, BASE_DIR

env.read_env(os.path.join(BASE_DIR, ".env"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='no-secret')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])


# Application definition
LOCAL_APPS = [
    'src.common.apps.CommonConfig',
    'src.authentication.apps.AuthConfig',
    'src.account.apps.UserConfig',
    'src.media.apps.UploadConfig',
    'src.customer.apps.CustomerConfig',
    'src.service.apps.ServiceConfig',
    'src.parametric.apps.ParametricConfig',
    'src.repair_shop.apps.RepairShopConfig',
    'src.financial.apps.FinancialConfig',
    'src.payment.apps.PaymentConfig',
    'src.geo.apps.GeoConfig',
    'src.communication.apps.CommunicationConfig',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'django_filters',
    'django_celery_results',
    'django_celery_beat',
    'corsheaders',
    'drf_spectacular',
    'django_extensions',
    'easy_thumbnails',
]

INSTALLED_APPS = [
    'channels',
    'daphne',

    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.inlines",  # optional, if special inlines are needed
    "unfold.contrib.import_export",  # optional, if django-import-export package is used
    "unfold.contrib.guardian",  # optional, if django-guardian package is used
    "unfold.contrib.simple_history",

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
    #'whitenoise.runserver_nostatic',       #it Can handle static file with django only
    'django.contrib.staticfiles',
    *THIRD_PARTY_APPS,
    *LOCAL_APPS,
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',         #it Can handle static file with django only
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'src.account.middleware.UpdateLastOnlineMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "src/templates/"),
        ],
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

# WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = "config.asgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': env.db('DATABASE_URL'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

if os.environ.get('GITHUB_WORKFLOW'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'github_actions',
            'USER': 'fixplus',
            'PASSWORD': '1234@1234',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
AUTH_USER_MODEL = 'authentication.User'

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
MEDIA_URL = '/media/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # Comment out JWTAuthentication if using session-based authentication
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'src.common.exception_handlers.custom_exception_handler',
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}


# Redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env("REDIS_LOCATION", default="redis://localhost:6379"),
    }
}
# Cache time to live is 15 minutes.
CACHE_TTL = 60 * 15


APP_DOMAIN = env("APP_DOMAIN", default="http://localhost:8000")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# SMS SERVICE
SMS_API_KEY = env("SMS_API_KEY")

from config.settings.cors import *  # noqa
from config.settings.jwt import *  # noqa
from config.settings.sessions import *  # noqa
from config.settings.celery import *  # noqa
from config.settings.swagger import *  # noqa
from config.settings.thumbnails import *
from config.settings.language import *
from config.settings.unfold import *