from os.path import join, normpath
from settings_common import *
from settings_sensitive import *

ALLOWED_HOSTS = ['localhost','crowdkitchen.io']
DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'crowdkitchen', # Or path to database file if using sqlite3.
        'USER': 'YOUR_DB_USER_NAME', # Not used with sqlite3.
        'PASSWORD': 'YOUR_DB_PASSWORD', # Not used with sqlite3.
        'HOST': '/Applications/MAMP/tmp/mysql/mysql.sock', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {
        "init_command": "SET foreign_key_checks = 0;",
        },
    }
}
# CrowdCafe_local
FACEBOOK_APP_ID = ''
FACEBOOK_API_SECRET = ''

GOOGLE_OAUTH2_CLIENT_ID      = ''
GOOGLE_OAUTH2_CLIENT_SECRET  = ''

GOOGLE_DISPLAY_NAME = ''

TWITTER_CONSUMER_KEY=''
TWITTER_CONSUMER_SECRET=''

GITHUB_APP_ID = ''
GITHUB_API_SECRET = ''

INSTAGRAM_CLIENT_ID = ''
INSTAGRAM_SECRET = ''

'''
FIREBASE = {
    'auth_token':'',
    'base_url':''
}
'''

BUSINESS = {
    'platform_owner_id': 1,
    'platform_commission': 0.3
}

'''
GOOGLE_ANALYTICS = {
    'account_id': '',
    'url': ''
}'''

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'WARN',
            'propagate': False,
        },
        'api': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        }, 'rest_framework': {
        'handlers': ['console'],
        'level': 'DEBUG',
        'propagate': True,
    }

    }
}