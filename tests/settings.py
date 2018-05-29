# -*- coding: utf-8
from __future__ import absolute_import, unicode_literals

DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '55555555555555555555555555555555555555555555555555'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',

    'tests',
]

SITE_ID = 1

MIDDLEWARE = ()
