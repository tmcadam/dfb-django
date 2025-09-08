from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from django.utils.safestring import mark_safe


from biographies.models import Biography, Country
from authors.models import BiographyAuthor
from comments.models import Comment
from images.models import Image

from imagekit.admin import AdminThumbnail


class ImageInline(admin.TabularInline):
    model = Image
    fields = ["title", "caption", "admin_thumbnail"]
    readonly_fields = ["title", "caption", "admin_thumbnail"]
    admin_thumbnail = AdminThumbnail(image_field="image100x100")
    show_change_link = True
    classes = ["collapse"]
    extra = 0
    max_num = 0
    can_delete = False


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0
    verbose_name = "Comment"
    verbose_name_plural = "Comments"
    show_change_link = True
    fields = [("name", "email"), "comment", ("created_at", "approved")]
    readonly_fields = ["created_at"]
    can_delete = False
    classes = ["collapse"]


class AuthorInline(admin.TabularInline):
    model = BiographyAuthor
    extra = 1
    verbose_name = "Author"
    verbose_name_plural = "Authors"
    show_change_link = True
    classes = ["collapse"]


class BiographyAdmin(SummernoteModelAdmin):
    search_fields = ["title", "authors"]
    list_display = ("title", "authors", "south_georgia", "featured", "biography_link")
    list_filter = ["featured"]

    summernote_fields = ("body", "external_links", "references")
    inlines = [AuthorInline, CommentInline, ImageInline]

    def biography_link(self, obj):
        return mark_safe(
            f'<a href="/biographies/{obj.slug}" target="_blank">/biographies/{obj.slug}</a>'
        )

    readonly_fields = ["biography_link"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("title", "featured", "biography_link"),
                    ("lifespan", "slug"),
                    ("primary_country", "secondary_country", "south_georgia"),
                    ("authors",),
                )
            },
        ),
        ("BODY", {"fields": ["body"], "classes": ["collapse"]}),
        (
            "ADDITIONAL INFORMATION",
            {
                "fields": ["external_links", "references", "revisions"],
                "classes": ["collapse"],
            },
        ),
    )


admin.site.register(Biography, BiographyAdmin)
admin.site.register(Country)
