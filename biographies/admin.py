from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import *

class BiographyAdmin(SummernoteModelAdmin):
    summernote_fields = ('body', 'external_links', 'references')

admin.site.register(Biography, BiographyAdmin)
admin.site.register(Country)