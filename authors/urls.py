from django.urls import path

from authors.views import AuthorsListView

app_name = "authors"
urlpatterns = [path("", AuthorsListView.as_view(), name="index")]
