from django.contrib import admin

from .models import Comment

# Register your models here.


class CommentAdmin(admin.ModelAdmin):
    list_display = ("biography", "name", "email", "approved", "created_at")
    list_filter = ("approved",)

    search_fields = ("name", "email", "comment", "biography__title")

    fieldsets = (
        (None, {"fields": ("biography", ("name", "email"), "comment", "approved")}),
    )


admin.site.register(Comment, CommentAdmin)
