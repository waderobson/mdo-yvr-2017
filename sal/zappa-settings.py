# Django settings for sal project.
from system_settings import *
import os

BASIC_AUTH = True
DEBUG = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sal',
        'USER': '<YOURDBUSERNAME>',
        'PASSWORD': '<YOURDBPASSWORD>',
        'HOST': '<RDS-HOSTNAME-GOES-HERE>',
        'PORT': 5432,
    }
}

# Needs to be changed to match the Zappa stage
# eg:
#   `zappa deploy prod`
# would mean you need to add `prod`
# to the LOGIN URLS
#
# LOGIN_URL='/prod/login'
# LOGIN_REDIRECT_URL='/prod/'
# Once you've deployed a custom domain you can then
# change back to Sals defaults
# LOGIN_URL='/login'
# LOGIN_REDIRECT_URL='/'

LOGIN_URL='/dev/login'
LOGIN_REDIRECT_URL='/dev/'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'sal',
    'server',
    'api',
    'catalog',
    'inventory',
    'licenses',
    'bootstrap3',
    'watson',
    'datatableview',
    'search',
    'storages'
)

LOGGING = {}

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

# Replace these setting with your own
AWS_STORAGE_BUCKET_NAME = 'sal-mdo-2017'
AWS_ACCESS_KEY_ID = 'AKIAJRSTEKYAEXAMPLE'
AWS_SECRET_ACCESS_KEY = 'Cgfomyn13Fa99bmRvIpdrlqc6pcPk9Y+EXAMPLE'
AWS_AUTO_CREATE_BUCKET = True

# Tell django-storages that when coming up with the URL for an item in S3 storage, keep
# it simple - just use this domain plus the path. (If this isn't set, things get complicated).
# This controls how the `static` template tag from `staticfiles` gets expanded, if you're using it.
# We also use it in the next setting.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# This is used by the `static` template tag from `static`, if you're using that. Or if anything else
# refers directly to STATIC_URL. So it's safest to always set it.
STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

# Tell the staticfiles app to use S3Boto storage when writing the collected static files (when
# you run `collectstatic`).

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
