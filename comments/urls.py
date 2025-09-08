from django.urls import path

from comments import views

app_name = "comments"
urlpatterns = [
    path("submit_comment", views.submit_comment, name="submit_comment"),
    path("approve/<str:approve_key>", views.approve_comment, name="approve_comment"),
]
