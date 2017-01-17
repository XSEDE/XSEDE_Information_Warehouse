"""
Django settings for xsede_warehouse project.

Generated by 'django-admin startproject' using Django 1.8.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
from logging.handlers import SysLogHandler

import json
if 'DJANGO_CONF' not in os.environ:
    print 'Missing DJANGO_CONF environment variable'
    sys.exit(1)
try:
    with open(os.environ['DJANGO_CONF'], 'r') as file:
        conf=file.read()
        file.close()
    CONF = json.loads(conf)
except (ValueError, IOError), e:
    print 'Failed to load DJANGO_CONF=%s' % os.environ['DJANGO_CONF']
    raise

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's2vm^0!d72vqrkye9lq+4=l(1z$)jo$-9bvr+-01235#f=@*-e'

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True
DEBUG = CONF['DEBUG']

#ALLOWED_HOSTS = []
ALLOWED_HOSTS = CONF['ALLOWED_HOSTS']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'glue2_db',
    'glue2_db_api',
    'glue2_provider',
    'monitoring_db.apps.MonitoringDbConfig',
    'monitoring_db_api.apps.MonitoringDbApiConfig',
    'monitoring_provider.apps.MonitoringProviderConfig',
    'monitoring_views_api.apps.MonitoringViewsApiConfig',
    'rdr_db',
    'xcsr_db',
    'goendpoint_api',
    'resource_status_api',
    'warehouse_views',
    'xdcdb',
    'xdinfo',
    'speedpage',
    'outages',
    'projectresources',
    'processing_status',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

if 'SUB_SITE' in CONF:
    SWAGGER_SETTINGS = {
        'api_path': '/%s' % CONF['SUB_SITE']
}

ROOT_URLCONF = 'xsede_warehouse.urls'

#    'DIRS': [],
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(os.path.dirname(__file__), '../templates')],
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

WSGI_APPLICATION = 'xsede_warehouse.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
# Inead have: alter role django_owner set search_path='django';
#        'OPTIONS': {
#            'options': '-c search_path=django'
#        },
        'NAME': 'warehouse',
        'USER': 'django_owner',
        'PASSWORD': CONF['DJANGO_PASS'],
        'HOST': 'localhost',
        'PORT': '',
    },
    'glue2': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
# Relies on: alter role glue2_owner set search_path='glue2';
        'NAME': 'warehouse',
        'USER': 'glue2_owner',
        'PASSWORD': CONF['GLUE2_PASS'],
        'HOST': 'localhost',
        'PORT': '',                    # Set to empty string for default.
    },
    'xcsr': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
# Relies on: alter role glue2_owner set search_path='glue2';
        'NAME': 'warehouse',
        'USER': 'xcsr_owner',
        'PASSWORD': CONF['XCSR_PASS'],
        'HOST': 'localhost',
        'PORT': '',                    # Set to empty string for default.
    }
}

DATABASE_ROUTERS = ['glue2_db.router.ModelDatabaseRouter',
                    'monitoring_db.router.ModelDatabaseRouter',]
from glue2_db.router import *
from monitoring_db.router import *

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

# Caching Configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'my-cache',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join( os.path.dirname(__file__),  '../static' ),
)

#
# Other stuff added by JP
#
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_RENDERER_CLASSES': [
       'rest_framework.renderers.JSONRenderer',
       'rest_framework.renderers.StaticHTMLRenderer',
       'rest_framework.renderers.BrowsableAPIRenderer',
       'rest_framework_xml.renderers.XMLRenderer',
#       'rest_framework.renderers.HTMLFormRenderer',
    ],
    'PAGINATE_BY': 10,
}

import logging

if DEBUG or not os.path.exists('/dev/log'):
    DEFAULT_LOG = 'console'
else:
    DEFAULT_LOG = 'syslog'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'syslog': {
            'format': 'weblate[%(process)d]: %(levelname)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'logfile': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        },
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s %(message)s',
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },'console': {
            'level': 'WARNING',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
	    'formatter': 'simple',
        },'dbfile': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': CONF['DB_LOG'],
        },'g2file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': CONF['G2_LOG'],
            'formatter': 'logfile',
            'when': 'W6',
            'backupCount': 999,
            'utc': True,
        }, 'syslog': {
            'level': 'WARNING',
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'syslog',
            'address': CONF['SYSLOG_SOCK'],
            'facility': SysLogHandler.LOG_LOCAL2,
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', DEFAULT_LOG],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {
            'level': 'WARNING',
            'handlers': ['dbfile'],
        },
#        'django.db.backends.postgresql_psycopg2': {
#            'level': 'DEBUG',
#            'handlers': ['console'],
#        },
        'xsede.glue2': {
            'level': 'INFO',
            'handlers': ['g2file'],
        },
    }
}

ADMINS = (
	('JP Navarro', 'navarro@mcs.anl.gov'),
	('Eric Blau', 'blau@mcs.anl.gov'),
)

logg2 = logging.getLogger('xsede.glue2')
logg2.setLevel(logging.DEBUG)

if DEBUG:
    logdb = logging.getLogger('django.db.backends')
    logdb.setLevel(logging.WARNING)
