# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from model_utils.models import TimeStampedModel

from autoslug import AutoSlugField
from djorm_hstore.models import HStoreManager
from djorm_hstore.fields import DictionaryField

from .conf import settings
from autoslug.utils import translit_long


def slugify(value):
    return translit_long(value).lower()

user_model_label = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')





class Officium(TimeStampedModel):
    """
    Container Model
    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = AutoSlugField(unique=True, populate_from='name', slugify=slugify)

    def __unicode__(self):
        return 'Officium of %(slug)s' % {'slug': self.slug}


class OfficiumSite(TimeStampedModel):
    """
    Officium Site
    """

    url = models.URLField(max_length=200)
    default = models.BooleanField()
    officium = models.ForeignKey(Officium, related_name='sites')

    def __unicode__(self):
        return 'OfficiumSite for %(officium)s' % {'officium': self.officium.slug}


class OfficiumUser(TimeStampedModel):
    """
    User profile for a specific officium
    """

    officium = models.ForeignKey(Officium, related_name='users')
    user = models.ForeignKey(user_model_label)
    is_manager = models.BooleanField()

    last_login = models.DateTimeField(null=True)
    profile_data = DictionaryField(db_index=True, null=True, blank=True)

    objects = HStoreManager()

    def __unicode__(self):
        return 'Profile of %(username)s' % {'username': self.user.username}
