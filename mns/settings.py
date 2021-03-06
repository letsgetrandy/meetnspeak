# Django settings for mns project.
import os
import dj_database_url


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DEBUG = bool(os.environ.get('DJANGO_DEBUG', ''))
GMAPS_KEY = os.environ.get('GMAPS_KEY', '')
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    ('Admin', os.environ.get('ADMIN_EMAIL', '')),
)

MANAGERS = ADMINS

APIHOST = str(os.environ.get('APIHOST', ''))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
DATABASES['default'] = dj_database_url.config(
        default='postgres://mnsowner:meetnspeak@localhost/meetnspeak'
    )
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''


AWS_ACCESS_KEY_ID = os.environ.get('S3_KEY')
AWS_SECRET_ACCESS_KEY = os.environ.get('S3_SECRET')
AWS_STORAGE_BUCKET_NAME = 'spikizi'
AWS_QUERYSTRING_AUTH = False

if DEBUG:
    STATIC_URL = '/static/'
    MEDIA_URL = ''
    STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

if not DEBUG:
    STATIC_URL = 'http://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/'
    MEDIA_URL = 'http://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/media/'
    STATICFILES_STORAGE = 'mns.storage.S3PipelineStorage'

#ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'collected_static/')


# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


#PIPELINE = False

PIPELINE_CSS = {
    'main': {
        'source_filenames': (
            'styles/mns.css',
        ),
        'output_filename': 'mns.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
    'ie': {
        'source_filenames': (
            'styles/ie.css',
        ),
        'output_filename': 'ie.css',
    },
}
PIPELINE_JS = {
    'main': {
        'source_filenames': (
            'scripts/mns.js',
            'scripts/*.js',
        ),
        'output_filename': 'mns.js',
    },
}
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.jsmin.JSMinCompressor'
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.cssmin.CSSminCompressor'


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'v8hik-8)sboec2wtsfw=w9s0*ixrg0c3n=+jg1l*m7cfk)3^rq'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mns.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'mns.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.static',
    'mns.context_processors.request_session',
    'mns.context_processors.site_settings',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pipeline',
    'mns',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        #'console': {
        #    'level': 'INFO',
        #    'class': 'logging.StreamHandler',
        #    'stream': 'sys.stdout',
        #},
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
