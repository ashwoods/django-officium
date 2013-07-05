# -*- coding: utf-8 -*-
from decorator import decorator
from officium.conf import settings


def officium(label):
    def officum(f, *args, **kwargs):
        return f(*args, **kwargs)

    return decorator(officium)

