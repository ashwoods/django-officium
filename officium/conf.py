# -*- coding: utf-8 -*-

import importlib

from django.conf import settings  # noqa
from django.core.exceptions import ImproperlyConfigured
from appconf import AppConf
gettext = lambda s: s

class OfficiumConf(AppConf):
    DECORATOR_MODULE = None
    TRY_SILENTLY = True

if settings.OFFICIUM_DECORATOR_MODULE is None:
    raise ImproperlyConfigured('OFFICIUM_DECORATOR_MODULE not found. Did you set it in settings.py?')
else:
    try:
        importlib.import_module(settings.OFFICIUM_DECORATOR_MODULE)
    except ImportError:
        raise ImproperlyConfigured('OFFICIUM_DECORATOR_MODULE set but could not be imported. Is it on sys.path?')

