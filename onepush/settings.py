"""
Django settings for onepush project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
# ^^^ The above is required if you want to import from the celery
# library.  If you don't have this then `from celery.schedules import`
# becomes `proj.celery.schedules` in Python 2.x since it allows
# for relative imports by default.

# Celery settings


ENV = os.getenv('ENV', 'LOCAL').upper()

db_host = '127.0.0.1'
db_user = 'root'
db_passwd = '123456'

# CELERY_BROKER_URL = 'amqp://guest:guest@localhost//'
# CELERY_BROKER_URL = 'redis://localhost//'

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
# CELERY_RESULT_BACKEND = 'db+sqlite:///results.sqlite'
CELERY_TASK_SERIALIZER = 'json'

CELERYD_CONCURRENCY = 2

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9y-ru9u0^lmwfaa^m(bnf489cmfai8n&!@f2ddva^bzodd(3)q'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

# Application definition

INSTALLED_APPS = [
    # 'polls.apps.PollsConfig',
    # 'uploads.apps.UploadsConfig',
    # 'hx.apps.HxConfig',
    'account.apps.AccountConfig',
    # 'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'blog',
    'mptt',
    # 'reverie.apps.ReverieConfig',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'onepush.utils.DisableCSRF',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'onepush.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
}

WSGI_APPLICATION = 'onepush.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'develop/db.sqlite3'),
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'onepush',
        'USER': db_user,
        # 'USER': 'root',
        'PASSWORD': db_passwd,
        # 'PASSWORD': '111',
        # 'HOST': 'rm-uf6piu9ry5sgv0z2lo.mysql.rds.aliyuncs.com',  # nzwh
        # 'HOST': 'rm-uf6piu9ry5sgv0z2l.mysql.rds.aliyuncs.com',  # nzwh
        'HOST': db_host,  # nzwh
        'PORT': '3306',
        'OPTIONS': {
            "init_command": "SET default_storage_engine=MyISAM",
        }
        # 'OPTIONS': {
        #     'sql_mode': 'traditional',
        # }
    }
}

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

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
CORS_ORIGIN_ALLOW_ALL = True

STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, "frontend/backstage/dist"),
    os.path.join(BASE_DIR, "/static"),
]

ATOMIC_REQUESTS = True
# APPEND_SLASH = False

CELERY_RESULT_BACKEND = 'redis://localhost'
# CELERY_TASK_RESULT_EXPIRES = 18000
# CELERY_RESULT_BACKEND = 'django-db'


CSRF_USE_SESSIONS = True

# DATABASES['OPTIONS']['init_command'] = "SET sql_mode='STRICT_TRANS_TABLES'"
CORS_ORIGIN_WHITELIST = (
    'google.com',
    'baidu.com',
)

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
#         },
#         'simple': {
#             'format': '%(levelname)s %(message)s'
#         },
#     },
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'formatter': 'verbose',
#             'filename': '/var/log/deepano/access_debug.log',
#         },
#         # 'console': {
#         #     'level': 'INFO',
#         #     'filters': ['require_debug_true'],
#         #     'class': 'logging.StreamHandler',
#         #     'formatter': 'verbose',
#         #     'filename': '/var/log/deepano/access_info.log',
#         # },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file', ],
#             'level': 'DEBUG',
#             'propagate': True,
#         }
#     }
# }

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

login_url = '/account/sign/in'
