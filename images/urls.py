from django.urls import path
from .views import ImageListView, ImageCreateView, ImageUpdateView

app_name = "images"
urlpatterns = [
    path("", ImageListView.as_view(), name="index"),
    path("new/", ImageCreateView.as_view(), name="new"),
    path("<int:pk>/edit/", ImageUpdateView.as_view(), name="edit"),
]
