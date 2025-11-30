"""
Django settings for project project.
"""

from pathlib import Path
import os
import dj_database_url # Import is already correct

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- CORE SECURITY SETTINGS ---

# SECURITY WARNING: The SECRET_KEY MUST be loaded from an environment variable!
# The 'django-insecure-local-key' is only a safe fallback for local development.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-local-key')

# SECURITY WARNING: Set this to 'False' on your production server.
# We check for the string 'True' for safety.
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'

# ALLOWED_HOSTS must list your domain(s) and IP address in production.
# The fallback list is intentionally empty for security when DEBUG is False.
ALLOWED_HOSTS = os.getenv(
    'ALLOWED_HOSTS',
    ''  # Safely fallback to an empty string to force failure if not set
).split(',')


# --- APPLICATION DEFINITION ---

INSTALLED_APPS = [
    # IMPORTANT: Removed 'whitenoise.runserver_nostatic' as it's only for dev server.
    'django.contrib.staticfiles',
    'statues.apps.StatuesConfig',
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise must be placed directly after SecurityMiddleware for best performance
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

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

WSGI_APPLICATION = 'project.wsgi.application'


# --- DATABASE CONFIGURATION (Production Ready) ---

# Use dj_database_url to configure the database from the DATABASE_URL environment variable.
# It falls back to SQLite for local development if DATABASE_URL is not set.
# conn_max_age is added for persistent connections (recommended for performance).
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
        conn_max_age=600 # 10 minutes connection age
    )
}


# --- PASSWORD VALIDATION ---
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# --- INTERNATIONALIZATION ---

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# --- STATIC FILES (WhiteNoise Configuration) ---
# WhiteNoise will serve static files efficiently in production.

STATIC_URL = '/static/'
# Where 'collectstatic' will put all files for WhiteNoise/Nginx to serve:
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 

# Use WhiteNoise's optimized storage class for compression and manifest hashing.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# --- MEDIA FILES (User-uploaded files) ---

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- CORS HEADERS ---

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # Add your PRODUCTION frontend domain(s) here (e.g., "https://yourfrontend.com")
]