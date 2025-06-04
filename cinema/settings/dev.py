from datetime import timedelta

from .common import *

DEBUG = True
SECRET_KEY = 'django-insecure-#mbo$vb9!+4s!$_f$e)sx%ddw+65^j2bslyqvkv%0$q0t6)4%r'

ALLOWED_HOSTS = ["0.0.0.0", "127.0.0.1", "localhost"]

MIDDLEWARE += ['silk.middleware.SilkyMiddleware', ]
INSTALLED_APPS += ['silk', 'debug_toolbar']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR.parent / 'db.sqlite3',
    }
}

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True

SESSION_COOKIE_SAMESITE = "None"

SESSION_COOKIE_SECURE = True

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=20),
}
