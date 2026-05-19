from django.urls import path

from . import views
from .views import PageCreateView, PageUpdateView

app_name = "pages"

urlpatterns = [
    path("", views.home, name="home"),
    path("new/", PageCreateView.as_view(), name="new"),
    path("<slug:page_slug>/edit/", PageUpdateView.as_view(), name="edit"),
    path("<slug:page_slug>", views.show, name="show"),
]
