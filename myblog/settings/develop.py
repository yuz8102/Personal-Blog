from .base import *
# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':'blog_db',
        'USER': 'root',
        'PASSWORD': 'admin1234',
        'HOST':'127.0.0.1',
        'PORT':'3306',
        'CONN_MAX_AGE':5*60,
        'OPTIONS': {'charset':'utf8mb4'}
    }
}