from pathlib import Path
from dotenv import load_dotenv
import os
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure--1ce=keqd$es+p)*3n&920j21waf065r5v@m$9q(7szu%p7e5r" #NOTE: crete a new secrete key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # my created apps
    "Product.apps.ProductConfig",
    "Store.apps.StoreConfig",
    "User.apps.UserConfig",
    "Cart.apps.CartConfig",
    # 3rd party apps
    "phonenumber_field",
    "django_bootstrap5",
    "crispy_forms",
    "crispy_bootstrap5",
]
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "OnlineStoreProject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR,'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # new context variables
                "Store.context_processors.nav_bar",
            ],
        },
    },
]

WSGI_APPLICATION = "OnlineStoreProject.wsgi.application"


# SQLite Database setting
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }


# Local PostgreSQL Database stting
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': os.environ.get("DB_NAME"), 
#         'USER': os.environ.get("DB_USER"),
#         'PASSWORD': os.environ.get("DB_PASSWORD"),
#         'HOST': os.environ.get("DB_HOST"), 
#         'PORT': os.environ.get("DB_PORT"),
#     }
# }


# Local PostgreSQL Database stting
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("DB_NAME"), 
        'USER': os.environ.get("DB_USER"),
        'PASSWORD': os.environ.get("DB_PASSWORD"),
        'HOST': os.environ.get("DB_HOST"), 
        'PORT': os.environ.get("DB_PORT"),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


STATICFILES_DIRS=[os.path.join(BASE_DIR, 'static')]
STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field


# Set Media files variables
MEDIA_ROOT= os.path.join(BASE_DIR,"media")
MEDIA_URL= "/media/"
FIXTURE_DIRS = ['fixtures/']

# model for authenticating users
AUTH_USER_MODEL = "User.CustomUser"
# the default login urls rather than accounts/login
LOGIN_URL = '/user/login/'
# url route to redirect to after login authentication
LOGIN_REDIRECT_URL="home-page"
# url route to redirect to after logout
LOGOUT_REDIRECT_URL = 'home-page'


# Email backend settings
EMAIL_BACKEND= "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST="smtp.gmail.com"
EMAIL_PORT=465
EMAIL_USE_SSL=True  
EMAIL_HOST_USER = os.environ.get("EMAIL_USERNAME")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASSWORD")

# AWS_SECRET_KEY_ID = os.environ.get('AWS_SECRET_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
# AWS_S3_SIGNATURE_NAME = os.environ.get('AWS_S3_SIGNATURE_NAME')
# AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACL = None
# AWS_S3_VERIFY=True


# inactive login sessison time limit
# SESSION_COOKIE_AGE = 600
# SESSION_SAVE_EVERY_REQUEST = True