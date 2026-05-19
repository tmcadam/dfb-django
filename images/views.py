from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from .models import Image
from .forms import ImageForm


class ImageListView(LoginRequiredMixin, ListView):
    model = Image
    template_name = "images/index.html"
    context_object_name = "images"
    paginate_by = 50


class ImageCreateView(LoginRequiredMixin, CreateView):
    model = Image
    form_class = ImageForm
    template_name = "images/form.html"
    success_url = reverse_lazy("images:index")


class ImageUpdateView(LoginRequiredMixin, UpdateView):
    model = Image
    form_class = ImageForm
    template_name = "images/form.html"
    success_url = reverse_lazy("images:index")
