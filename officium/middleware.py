# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from .models import ApplicationProfile
import warnings

class OfficiumMiddleware(object):
    """
    Branding for awards. Sets MITTO_MIDDELWARE_AWARD.
    """
    def process_request(self, request):
        """
        Branding middleware for awards
        """

        # allows to set the application profile via environment variable or settings

        ENV_APP = getattr(settings, 'OFFICIUM_APPLICATION_PROFILE', None)

        if ENV_APP:
            request.OFFICIUM_MIDDLEWARE_PROFILE = ApplicationProfile.objects.get(name=ENV_APP)
            return None
        http_host = request.META.get('HTTP_HOST','').split(':')[0]
        request_domain = unicode(http_host)

        if request_domain.startswith('localhost') or request_domain.startswith('127'):
            host = 'localhost'
            request.OFFICIUM_MIDDLEWARE_PROFILE = None
        else:
            try:
                app_profile = ApplicationProfile.objects.get(url__iexact=request_domain) #TODO: Cache this
            except ApplicationProfile.DoesNotExist:
                app_profile = None
            request.OFFICIUM_MIDDLEWARE_PROFILE = app_profile
        return None
