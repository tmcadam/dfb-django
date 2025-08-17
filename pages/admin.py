from django.contrib import admin
from django.utils.safestring import mark_safe
from django_summernote.admin import SummernoteModelAdmin

from .models import Page

@admin.register(Page)
class PageAdmin(SummernoteModelAdmin):
    list_display = ('title', 'page_link')
    summernote_fields = ('body',)

    def page_link(self, obj):
        return mark_safe(f'<a href="/{obj.slug}" target="_blank">/{obj.slug}</a>')

    def get_readonly_fields(self, request, obj = ...):

        return super().get_readonly_fields(request, obj)
