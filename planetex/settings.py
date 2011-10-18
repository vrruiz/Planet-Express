# Django settings for planetex project.

DEBUG = False

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
    ('rvr','rvr')
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3' # 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = './db/planetex.db'             # Or path to database file if using sqlite3.
#DATABASE_NAME=''
#DATABASE_ENGINE=''
#DATABASE_USER = ''             # Not used with sqlite3.
#DATABASE_PASSWORD = ''         # Not used with sqlite3.
#DATABASE_HOST = 'localhost'             # Set to empty string for localhost. Not used with sqlite3.
#DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'Atlantic/Canary'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 's4&#x-*cgvfmxsb+@&_*4cya7=%x-7=@yilf3t3w^v1kjv#z(c'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.core.template.loaders.filesystem.load_template_source',
    'django.core.template.loaders.app_directories.load_template_source',
#     'django.core.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    "django.middleware.cache.CacheMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.sessions.SessionMiddleware",
    "django.middleware.doc.XViewMiddleware",
)

ROOT_URLCONF = 'planetex.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates".
    '/home/rvr/django/planetex/templates/',
)

INSTALLED_APPS = (
    'planetex.apps.planetex',
    'planetex.apps.planetex.contrib',
    'django.contrib.admin',
)

# rvr
CACHE_BACKEND = './cache/'
CACHE_MIDDLEWARE_SECONDS = 300
CACHE_MIDDLEWARE_KEY_PREFIX='planetex'
