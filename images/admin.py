from django.contrib import admin
from imagekit.admin import AdminThumbnail
from images.models import Image

# Register your models here.
from django_summernote.admin import SummernoteModelAdmin


class ImageAdmin(SummernoteModelAdmin):
    summernote_fields = ("caption",)
    list_display = ("biography__title", "title", "admin_thumbnail")

    search_fields = ["title", "biography__title"]
    admin_thumbnail = AdminThumbnail(image_field="image100x100")


admin.site.register(Image, ImageAdmin)
