"""
Django settings for xsede_warehouse project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

import json
if 'DJANGO_CONF' not in os.environ:
    print('Missing DJANGO_CONF environment variable')
    sys.exit(1)
try:
    with open(os.environ['DJANGO_CONF'], 'r') as file:
        conf=file.read()
    CONF = json.loads(conf)
except (ValueError, IOError) as e:
    print('Failed to load DJANGO_CONF={}'.format(os.environ['DJANGO_CONF']))
    raise
    
SETTINGS_MODE = CONF.get('SETTINGS_MODE', 'SERVER')

# SECURITY WARNING: keep the secret key used in production secret!
# Generated using: manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'
SECRET_KEY = CONF['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CONF['DEBUG']

TEST_SERVER = CONF.get('TEST_SERVER', None)
# Application definition

INSTALLED_APPS = (
    'allocations',
    'glue2_db',
    'glue2_db_api',
    'glue2_provider',
    'glue2_views_api',
    'goendpoint_api',
    'monitoring_db.apps.MonitoringDbConfig',
    'monitoring_db_api.apps.MonitoringDbApiConfig',
    'monitoring_provider.apps.MonitoringProviderConfig',
    'monitoring_views_api.apps.MonitoringViewsApiConfig',
    'outages',
    'processing_status',
    'projectresources',
    'rdr_db',
    'resource_v3',
    'resource_status_api',
    'speedpage',
    'warehouse_views',
    'xcsr_db',
    'xdcdb',
    'xdinfo',
)
#INSTALLED_APPS_RETIRED = (
#    'resource_cat',
#    'resource_v2',
#)

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

WRITE_HOSTNAME = CONF.get('DB_HOSTNAME_WRITE', 'infodb.xsede.org')
READ_HOSTNAME = CONF.get('DB_HOSTNAME_READ', 'infodb.xsede.org')

# Relies on: alter role django_owner set search_path='django';
# Relies on: alter role glue2_owner set search_path='glue2';
# Relies on: alter role xcsr_owner set search_path='glue2';
DATABASES = {       # Set common NAME, ENGINE, PORT, CONN_MAX_AGE below
    'default': {
        'USER': 'django_owner',
        'PASSWORD': CONF['DJANGO_PASS'],
        'HOST': WRITE_HOSTNAME,
    },
    'default.read': {
        'USER': 'django_owner',
        'PASSWORD': CONF['DJANGO_PASS'],
        'HOST': READ_HOSTNAME,
    },
    'glue2': {
        'USER': 'glue2_owner',
        'PASSWORD': CONF['GLUE2_PASS'],
        'HOST': WRITE_HOSTNAME,
    },
    'glue2.read': {
        'USER': 'glue2_owner',
        'PASSWORD': CONF['GLUE2_PASS'],
        'HOST': READ_HOSTNAME,
    },
    'xcsr': {
        'USER': 'xcsr_owner',
        'PASSWORD': CONF['XCSR_PASS'],
        'HOST': WRITE_HOSTNAME,
    },
    'xcsr.read': {
        'USER': 'xcsr_owner',
        'PASSWORD': CONF['XCSR_PASS'],
        'HOST': READ_HOSTNAME,
    }
}

for db in DATABASES:
    DATABASES[db]['NAME'] = 'warehouse'
    DATABASES[db]['ENGINE'] = 'django.db.backends.postgresql'
    DATABASES[db]['PORT'] = ''
    DATABASES[db]['CONN_MAX_AGE'] = 600 # Persist DB connections

DATABASE_ROUTERS = ['xsede_warehouse.router.ModelDatabaseRouter',]
from xsede_warehouse.router import *

if CONF.get('ELASTIC_HOSTS'):
    import elasticsearch_dsl.connections
    from elasticsearch import Elasticsearch, RequestsHttpConnection
    ELASTICSEARCH_DSL = {
        'default': {
            'hosts': CONF.get('ELASTIC_HOSTS', None)
        },
    }
    ESCON = elasticsearch_dsl.connections.create_connection( \
        hosts = CONF['ELASTIC_HOSTS'], \
        connection_class = RequestsHttpConnection, \
        timeout = 10)
else:
    ESCON = None

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Logging setup

import logging
from logging.handlers import SysLogHandler

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
        },
        'console': {
            'level': 'WARNING',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'dbfile': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': CONF['DB_LOG'],
        },
        'g2file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': CONF['G2_LOG'],
            'formatter': 'logfile',
        },
        'syslog': {
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
            'level': 'DEBUG',
            'handlers': ['dbfile'],
        },
        'xsede.logger': {
            'level': 'INFO',
            'handlers': ['g2file'],
        },
    }
}

ADMINS = (
	('Information Services Alerts', 'info-serv-alert@xsede.org'),
)

logg2 = logging.getLogger('xsede.logger')
logg2.setLevel(logging.DEBUG)

if DEBUG:
    logdb = logging.getLogger('django.db.backends')
    logdb.setLevel(logging.WARNING)

################################################################################
#
# Additional API settings
#
if SETTINGS_MODE == 'SERVER':
    API_BASE = CONF.get('API_BASE', '')

    #ALLOWED_HOSTS = []
    ALLOWED_HOSTS = CONF['ALLOWED_HOSTS']

    INSTALLED_APPS += (
        'corsheaders',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'mp_auth',
        'rest_framework',
        'drf_spectacular',
        'social_django',
    )

#        'django.middleware.cache.UpdateCacheMiddleware',
#        'django.middleware.cache.FetchFromCacheMiddleware',
    MIDDLEWARE = (
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

# Switched to True on 09-03-2020 by JP, making whitelist no longer relevant
    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ORIGIN_WHITELIST = (
        'https://xsede.org',
        'https://www.xsede.org',
        'https://portal.xsede.org',
        'https://resttesttest.com',
        'https://test-cors.org',
    )
    CORS_ALLOW_METHODS = (
        'GET'
    )

#from xsede_warehouse.apidoc_filter import filter_internal_apis
    SPECTACULAR_SETTINGS = {
        'TITLE': 'XSEDE Information Services API',
        'DESCRIPTION': 'Provides API access to XSEDE aggregated information services',
        'VERSION': '1.0.0',
        'PREPROCESSING_HOOKS': ['xsede_warehouse.hooks.remove_internal_apis'],
    }
    
    ROOT_URLCONF = 'xsede_warehouse.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [ os.path.normpath(os.path.join(os.path.dirname(__file__), '../templates'))],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    'social_django.context_processors.backends',
                    'social_django.context_processors.login_redirect',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'xsede_warehouse.wsgi.application'

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
        },
        'server': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': 'unix:/var/run/memcached/memcached.sock',
        }
    }
    
    # If configured CACHE_SERVER as True
    if CONF.get('CACHE_SERVER', False):
        CACHE_SERVER = 'server'
    else:
        CACHE_SERVER = 'default'
        
    # Static files (CSS, JavaScript, Images)

    STATIC_URL = '/static/'

    STATIC_ROOT = CONF.get('STATIC_ROOT', None)

    STATICFILES_DIRS = (
        os.path.join( os.path.dirname(__file__),  '../static' ),
    )

    #
    # Other stuff added by JP
    #
    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        ],
        'DEFAULT_RENDERER_CLASSES': [
           'rest_framework.renderers.JSONRenderer',
           'rest_framework.renderers.StaticHTMLRenderer',
           'rest_framework.renderers.BrowsableAPIRenderer',
           'rest_framework_xml.renderers.XMLRenderer',
        ],
        'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
        'PAGINATE_BY': 10,
    }

    MULTIPROVIDER_AUTH = {
        "BearerTokens": {
            "globus": {
                "scope": ["openid"],
                "aud": "xsede_info_servers_oauth",
            }
        },
    }
    from xsede_warehouse.globus_oauth_toolkit import *

    #
    # Social Auth
    #
    SOCIAL_AUTH_POSTGRES_JSONFIELD = True
    SOCIAL_AUTH_URL_NAMESPACE = 'social'
    SOCIAL_AUTH_GLOBUS_KEY = '1b5eb438-f4a8-4835-9696-d8ffa53cd6b7'
    SOCIAL_AUTH_GLOBUS_SECRET = CONF['SOCIAL_AUTH_GLOBUS_SECRET']
    SOCIAL_AUTH_GLOBUS_AUTH_EXTRA_ARGUMENTS = {
        'access_type': 'offline',
    }

    #
    #Multiprovider Auth
    #
    GLOBUS_CLIENT_ID = SOCIAL_AUTH_GLOBUS_KEY
    GLOBUS_CLIENT_SECRET = SOCIAL_AUTH_GLOBUS_SECRET

    AUTHENTICATION_BACKENDS = (
        'social_core.backends.globus.GlobusOpenIdConnect',
        'django.contrib.auth.backends.ModelBackend',
    )

    LOGIN_URL = 'login'
    LOGIN_REDIRECT_URL = 'home'
