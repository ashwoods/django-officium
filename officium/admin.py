# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import *

class ApplicationModuleAdmin(admin.ModelAdmin):
    pass


class ApplicationThemeAdmin(admin.TabularInline):
    model = ApplicationTheme


class ApplicationProfileAdmin(admin.ModelAdmin):
    inlines = (ApplicationThemeAdmin,)


admin.site.register(ApplicationFeature, ApplicationModuleAdmin)
admin.site.register(ApplicationProfile, ApplicationProfileAdmin)
