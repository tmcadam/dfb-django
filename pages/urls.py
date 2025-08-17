from django.urls import path

from biographies.views import show_by_slug
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:page_slug>', views.show, name='show'),
]
