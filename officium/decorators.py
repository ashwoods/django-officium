# -*- coding: utf-8 -*-
from decorator import decorator
import importlib

from officium.conf import settings



def officium_method(relation, label=None):
    def call(self, object, officium_relation=relation, officium_label=label, *args, **kwargs):
        function = self
        officium = reduce(getattr, officium_relation.split('.'), object)

        try:
            function = getattr(importlib.import_module('%s.%s' % (settings.OFFICIUM_DECORATOR_MODULE, officium.slug)),
                               officium_label)
        except (AttributeError, ImportError), e:
            if settings.OFFICIUM_TRY_SILENTLY:
                pass
            else:
                raise

        return function(object, *args, **kwargs)
    return decorator(call)

