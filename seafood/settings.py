import json
import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-90t+ia0awso=tr&xi2nmcgq9v$i-w#64%r7n62+ui4xj0s_ps&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    'seafood-4308.onrender.com',
    '127.0.0.1',
    'localhost',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third Party Apps
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'corsheaders',
    'whitenoise.runserver_nostatic',
    'django_crontab',
    # Custom Apps
    'users',
    'shipments',
    'supplierpurchases',
    'logisticsreceipts',
    'sales',
    'costledgers',
    'currencies',
    'payments',
    'exchangerates',
    'unitofmeasures',
    'productcategories',
    'products',
    'notifications',
    'audit',
    'configuration',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'seafood.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'seafood.wsgi.application'

CORS_ALLOW_ALL_ORIGINS = True # For development only
CORS_ALLOW_CREDENTIALS = True

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases



DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/
AUTH_USER_MODEL = "users.User"
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/6.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'seafood.pagination.StandardResultsSetPagination',
    'PAGE_SIZE': 5,
}

# ADMIN CREDENTIALS
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD =  os.getenv("ADMIN_PASSWORD")
ADMIN_LOCATION = os.getenv("ADMIN_LOCATION", "Headquarters")

# AWS Storage
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME', 'seafood')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')

# ADMIN_ROLES = os.getenv("ADMIN_ROLES", "Admin").split(",")
ADMIN_ROLES = os.getenv("ADMIN_ROLES", "Admin")
ROLE_CAPABILITIES = json.loads(
    os.getenv("ROLE_CAPABILITIES_JSON", "{}")
)
# CRON JOBS
# Run sync_rates every hour
CRONJOBS = [
    ('0 * * * *', 'django.core.management.call_command', ['sync_rates']),
]

# FRONTEND SETTINGS
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "noreply@seafood.com")

# EMAIL CONFIGURATION (Using console for development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
