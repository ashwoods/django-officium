# -*- coding: utf-8 -*-

from django.db import models
from model_utils.managers import PassThroughManager
from model_utils import Choices
from model_utils.models import TimeStampedModel
from sitetree.models import Tree
from filebrowser.fields import FileBrowseField
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib.auth.models import Group, User

import os


class ApplicationFeature(models.Model):
    """Available features or modules that can be added dynamically to an application"""
    name = models.CharField(max_length=50)
    menus = models.ManyToManyField(Tree, null=True, blank=True)

    def __unicode__(self):
        return self.name


class ApplicationProfile(TimeStampedModel):
    """Application Profile that allows configuring theme, active apps, and branding"""

    name = models.SlugField(max_length=100)
    url = models.URLField()
    features = models.ManyToManyField(ApplicationFeature)


    admins = models.ForeignKey(Group)

    def __unicode__self(self):
        return self.url


class ApplicationTheme(models.Model):
    """Here we can put the values we need for branding an app"""

    THEME_PATH = os.path.join(settings.PROJECT_ROOT, 'apps', 'layouts', 'themes')
    THEME_TYPES = Choices(
                        ('admin', _('admin')),
                        ('whitelabel', _('whitelabel')),
                        ('landing', _('landing'))
    )

    app = models.ForeignKey(ApplicationProfile)

    # once django 1.5 comes out
    theme = models.FilePathField(path=THEME_PATH, allow_folders=True, allow_files=False, blank=True)


    @property
    def theme(self):
        pass  # TODO: finish this!


class UserApplicationProfile(TimeStampedModel):
    """Registration of the user to a specific application profile"""

    user = models.ForeignKey(User)
    application_profile = models.ForeignKey(ApplicationProfile)
