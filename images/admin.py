from django.contrib import admin
from imagekit.admin import AdminThumbnail
from .models import *
# Register your models here.

class ImageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'admin_thumbnail')
    admin_thumbnail = AdminThumbnail(image_field='image100x100')

admin.site.register(Image, ImageAdmin)