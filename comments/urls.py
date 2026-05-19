from django.urls import path
from . import views
from .views import CommentListView, CommentUpdateView

app_name = "comments"
urlpatterns = [
    path("", CommentListView.as_view(), name="index"),
    path("<int:pk>/edit/", CommentUpdateView.as_view(), name="edit"),
    path("submit_comment", views.submit_comment, name="submit_comment"),
    path("approve/<str:approve_key>", views.approve_comment, name="approve_comment"),
]
