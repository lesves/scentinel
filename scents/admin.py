from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from . import models


class AttachmentInline(admin.TabularInline):
	model = models.Attachment


class ScentAdmin(GISModelAdmin):
	inlines = [AttachmentInline]

admin.site.register(models.Scent, ScentAdmin)
