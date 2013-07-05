# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import *

class OfficiumSiteInline(admin.StackedInline):
    model = OfficiumSite

class OfficiumAdmin(admin.ModelAdmin):
    inlines = [OfficiumSiteInline]

class OfficiumUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(OfficiumUser, OfficiumUserAdmin)
admin.site.register(Officium, OfficiumAdmin)


