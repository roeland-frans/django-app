import os
import ssl

from datetime import timedelta
from pathlib import Path
from socket import gethostbyname
from socket import gethostname

# Your app version
VERSION = "0.0.1"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = (
    "django-insecure-o@9x-=l(bfn^game*a725o&7g!x3n7o3iv9k%&$5(_w_agmju7"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = []
if os.getenv("CLUSTER") == "True":
    ALLOWED_HOSTS += [gethostname(), gethostbyname(gethostname())]
ALLOWED_HOSTS += ["127.0.0.1", "localhost"]
ALLOWED_CIDR_NETS = ["172.0.0.0/8", "10.0.0.0/8", "192.168.0.0/12"]

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*YOUR_DOMAIN$",
]

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_REDIRECT_EXEMPT = [r"^_health/$"]

INSTALLED_APPS = [
    "app.apps.AppConfig",
    "app.apps.AppAdminConfig",
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "allow_cidr.middleware.AllowCIDRMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if os.getenv("RDS_HOSTNAME") is not None:
    if Path("~/.postgresql/root.crt").exists():
        options = {
            "sslmode": "verify-full",
        }
    else:
        options = {}

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("RDS_DB_NAME"),
            "USER": os.getenv("RDS_USERNAME"),
            "PASSWORD": os.getenv("RDS_PASSWORD"),
            "HOST": os.getenv("RDS_HOSTNAME"),
            "PORT": os.getenv("RDS_PORT"),
            "CONN_MAX_AGE": 120,
            "OPTIONS": options,
        }
    }
    SQLITE_DB = False
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_HOSTNAME = os.getenv("REDIS_HOSTNAME")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = os.getenv("REDIS_DB")
REDIS_SSL = os.getenv("REDIS_SSL", "False") == "True"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
AUTH_USER_MODEL = "app.User"

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

STATIC_ROOT = os.path.join(BASE_DIR, "static")

DEFAULT_FILE_STORAGE = "storages.backends.s3.S3Storage"
MEDIA_ROOT = "media/"
MEDIA_URL = os.getenv("MEDIA_URL", "/media/")

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME", "")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME", "")
AWS_S3_CUSTOM_DOMAIN = os.getenv("AWS_S3_CUSTOM_DOMAIN", "")
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_CLOUDFRONT_KEY_ID = os.getenv("AWS_CLOUDFRONT_KEY_ID", "")
AWS_CLOUDFRONT_KEY = os.getenv("AWS_CLOUDFRONT_KEY", "")

if REDIS_SSL:
    CELERY_BROKER_URL = (
        f"rediss://:{REDIS_PASSWORD}@{REDIS_HOSTNAME}:{REDIS_PORT}/{REDIS_DB}"
    )
    CELERY_BROKER_USE_SSL = {
        "ssl_cert_reqs": ssl.CERT_REQUIRED,
    }
else:
    CELERY_BROKER_URL = (
        f"redis://:{REDIS_PASSWORD}@{REDIS_HOSTNAME}:{REDIS_PORT}/{REDIS_DB}"
    )

CELERY_BROKER_TRANSPORT_OPTIONS = {"global_keyprefix": "{celery}:"}
CELERY_RESULT_BACKEND = "django-db"
CELERY_RESULT_EXTENDED = True
CELERY_RESULT_EXPIRES = timedelta(hours=48)
CELERY_TASK_ALWAYS_EAGER = False
CELERY_WORKER_LOG_COLOR = True
CELERY_WORKER_REDIRECT_STDOUTS = False

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "noreply@YOUR_DOMAIN")
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "")
EMAIL_PORT = os.getenv("EMAIL_PORT", "587")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = True

GRAPHENE = {
    "SCHEMA": "app.api.schema.schema",
    "MIDDLEWARE": ["graphql_jwt.middleware.JSONWebTokenMiddleware"],
}

GRAPHQL_JWT = {
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
    "JWT_EXPIRATION_DELTA": timedelta(hours=48),
    "JWT_REFRESH_EXPIRATION_DELTA": timedelta(days=60),
    "JWT_COOKIE_NAME": "WS",
    "JWT_REFRESH_TOKEN_COOKIE_NAME": "WS-R",
    "JWT_COOKIE_SECURE": True,
    "JWT_COOKIE_PATH": "/",
    "JWT_COOKIE_DOMAIN": None,
}
JWT_COOKIE_ENCRYPTION_KEY = os.getenv("JWT_COOKIE_ENCRYPTION_KEY", "XXX")
JWT_COOKIE_SAME_SITE = os.getenv("JWT_COOKIE_SAME_SITE", "none")

SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "strict")
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 30 * 60  # 30 minutes
