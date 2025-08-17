from django.urls import path

from .views import index, show_by_slug, show_by_id

app_name = "biographies"
urlpatterns = [
    path("", index, name="index"),
    path("<int:bio_id>", show_by_id, name="show_by_id"),
    path("<slug:bio_slug>", show_by_slug, name="show"),
]
