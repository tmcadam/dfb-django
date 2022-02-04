from django.urls import path

from . import views

app_name = 'biographies'
urlpatterns = [
    path('<slug:bio_slug>/', views.show, name='show'),
]
