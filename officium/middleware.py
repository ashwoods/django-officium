# -*- coding: utf-8 -*-
from urlparse import urlsplit

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from .models import Officium, OfficiumUser, OfficiumSite
import warnings


class OfficiumMiddleware(object):
    """
    Officium Site Middleware allows you to have independent sites depending on the request url
    """
    def process_request(self, request):

        if request.path.startswith(settings.OFFICIUM_IGNORE_PATHS):
            return None

        officium = None

        # first try default test or default officium in settings.py
        officium_setting = getattr(settings, 'OFFICIUM_SITE', None)

        if officium_setting:
            try:
                officium_site = OfficiumSite.objects.get(url__iexact="http://%s/" % officium_setting)
                officium = officium_site.officium
            except OfficiumSite.DoesNotExist:
                pass

        else:
            http_host = request.META.get('HTTP_HOST', '').split(':')[0]
            request_domain = unicode(http_host)

            if request_domain.startswith('localhost') or request_domain.startswith('127'):
                request.OFFICIUM = None

            else:
                try:
                    officium_site = OfficiumSite.objects.get(url__icontains=request_domain)
                    officium = officium_site.officium
                except OfficiumSite.DoesNotExist:
                    pass

        if request.user.is_authenticated():
            try:
                officium_user = OfficiumUser.objects.get(user=request.user, officium=officium)
            except:
                officium_user = None
        else:
            officium_user = None

        request.OFFICIUM = officium
        request.OFFICIUM_USER = officium_user
        return None
