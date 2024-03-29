import os
from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5crx$2#@-^fcme(fn!*#%ra@3^v!qb+0n40*a-af&(w499f&i3'
#SECRET_KEY = os.environ.get('SECRET_KEY', 'your_current_secret_key_value')
# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True
WEBSITE_HOSTNAME = os.environ.get('WEBSITE_HOSTNAME', None)

DEBUG = WEBSITE_HOSTNAME == None

if DEBUG:
    ALLOWED_HOSTS = []
else:
    ALLOWED_HOSTS = [WEBSITE_HOSTNAME]
    CSRF_TRUSTED_ORIGINS = [f'https://{WEBSITE_HOSTNAME}']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bus.apps.BusConfig',
    'users.apps.UsersConfig',
    'reviews.apps.ReviewsConfig',
    'crispy_forms',
    'crispy_bootstrap4',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'pwa',
    'widget_tweaks'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware'
]

ROOT_URLCONF = 'busApp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
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

WSGI_APPLICATION = 'busApp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['AZURE_DB_NAME'],
        'HOST': os.environ['AZURE_DB_HOST'],
        'PORT': os.environ['AZURE_DB_PORT'],
        'USER': os.environ['AZURE_DB_USER'],
        'PASSWORD': os.environ['AZURE_DB_PASSWORD'],
        
    }
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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
DEFAULT_FILE_STORAGE = 'busApp.storage.AzureMediaStorage'
STATICFILES_STORAGE = 'busApp.storage.AzureStaticStorage'

STATIC_LOCATION = "static"
MEDIA_LOCATION = "media"

AZURE_ACCOUNT_NAME = "c2063081"
AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'
STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/'

# Adjust the following settings for Azure Storage
AZURE_ACCOUNT_KEY = 'H25Y8tmCnZFNVvOSYzkuNlCGAFwqEt+nFiZXbeD9l3KUF95b3OU1e8mrBZhMGjaG8UO3UyEe/ktT+AStFrdNEQ=='  # Replace with your Azure Storage account key
AZURE_CONTAINER = 'c2063081'  # Replace with your Azure Storage container name

AZURE_BLOB_HEADERS = {
    'x-ms-blob-cache-control': 'max-age=3600',  # Adjust cache settings as needed
    'Access-Control-Allow-Origin': '*',  # Set appropriate CORS policy
}

AZURE_OVERWRITE_FILES = True  # Set to True to overwrite existing files during collectstatic

#STATIC_URL = '/static/'
# MEDIA_ROOT = BASE_DIR / 'media'
# MEDIA_URL = '/media/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
#STATICFILES_DIRS = [
#    os.path.join(BASE_DIR, 'static'),
#]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CRISPY_ALLOWED_TEMPLATE_PACK = 'bootstrap4'
CRISPY_TEMPLATE_PACK = 'bootstrap4'
LOGIN_URL = 'login'
LOGIN_TEMPLATE = 'login'
LOGIN_REDIRECT_URL = 'route_plan'
LOGOUT_REDIRECT_URL = '/'

# allauth settings
ACCOUNT_AUTHENTICATION_METHOD = 'email'  # or 'username' or other methods
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
SOCIALACCOUNT_QUERY_EMAIL = ACCOUNT_EMAIL_REQUIRED
SOCIALACCOUNT_AUTO_SIGNUP = True  # Automatically create accounts for new users
SOCIALACCOUNT_LOGIN_ON_GET=True


PWA_APP_NAME = 'SmartBus Buddy'
PWA_APP_DESCRIPTION = 'Bus Application with smart review feature that suggest optima route.'
PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'static/js', 'serviceworker.js')
PWA_APP_THEME_COLOR = '#000000'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
	{
		'src': 'static/img/icon.png',
		'sizes': '160x160'
	}
]
PWA_APP_ICONS_APPLE = [
	{
		'src': 'static/img/icon.png',
		'sizes': '160x160'
	}
]
PWA_APP_SPLASH_SCREEN = [
	{
		'src': 'static/img/icon.png', 
		'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
	}
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'



AUTHENTICATION_BACKENDS = (
    # ...
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '624437417330-k6c0bdog1aokp3j2uv7ff5sl3li1l2ps.apps.googleusercontent.com',
            'secret': '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',
            'key': '',
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

AUTHENTICATION_CLASSES = (
    # ...
    'allauth.socialaccount.providers.oauth2.client.OAuth2ErrorRedirectHandler',
)

handler404 = 'bus.views.error'
