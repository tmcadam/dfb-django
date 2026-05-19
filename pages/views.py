from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.shortcuts import render, get_object_or_404
from biographies.models import Biography
from pages.models import Page
from .forms import PageForm


# Create your views here.
def home(request):
    featured_bios = Biography.objects.filter(featured=True)
    return render(request, "pages/home.html", context={"featured_bios": featured_bios})


def show(request, page_slug):
    page = get_object_or_404(Page, slug=page_slug)
    return render(request, "pages/show.html", context={"page": page})


class PageCreateView(LoginRequiredMixin, CreateView):
    model = Page
    form_class = PageForm
    template_name = "pages/form.html"
    success_url = reverse_lazy("pages:home")


class PageUpdateView(LoginRequiredMixin, UpdateView):
    model = Page
    form_class = PageForm
    template_name = "pages/form.html"
    slug_field = "slug"
    slug_url_kwarg = "page_slug"
    success_url = reverse_lazy("pages:home")
