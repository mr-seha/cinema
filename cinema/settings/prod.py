import os
from datetime import timedelta

from .common import *

DEBUG = False
SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = ["127.0.0.1"]

CORS_ALLOWED_ORIGINS = [
    # "https://example.com",
]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}
