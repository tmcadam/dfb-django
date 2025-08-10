from django.contrib import admin
from django.template.defaultfilters import truncatechars

from .models import Author, BiographyAuthor
# Register your models here.


class AuthorAdmin(admin.ModelAdmin):

    search_fields = ['first_name', 'last_name']
    list_display = ('__str__', 'short_biography',)

admin.site.register(Author, AuthorAdmin)

