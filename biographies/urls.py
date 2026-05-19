from django.urls import path

from .views import index, show_by_slug, show_by_id, BiographyCreateView, BiographyUpdateView, BiographyDeleteView, reset_featured, check_links, manage_biographies, make_featured, validate_slug, add_country_htmx, add_author_htmx

app_name = "biographies"
urlpatterns = [
    path("", index, name="index"),
    path("manage/", manage_biographies, name="manage"),
    path("new/", BiographyCreateView.as_view(), name="new"),
    path("reset_featured/", reset_featured, name="reset_featured"),
    path("check_links/", check_links, name="check_links"),
    path("validate_slug/", validate_slug, name="validate_slug"),
    path("add-country/", add_country_htmx, name="add_country_htmx"),
    path("add-author/", add_author_htmx, name="add_author_htmx"),
    path("<int:bio_id>", show_by_id, name="show_by_id"),
    path("<slug:bio_slug>", show_by_slug, name="show"),
    path("<slug:bio_slug>/edit/", BiographyUpdateView.as_view(), name="edit"),
    path("<slug:bio_slug>/delete/", BiographyDeleteView.as_view(), name="delete"),
    path("<slug:bio_slug>/make_featured/", make_featured, name="make_featured"),
]
