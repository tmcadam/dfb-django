from django.shortcuts import render, get_object_or_404
from biographies.models import Biography
from pages.models import Page


# Create your views here.
def home(request):
    featured_bios = Biography.objects.filter(featured=True)
    return render(request, "pages/home.html", context={"featured_bios": featured_bios})


def show(request, page_slug):
    page = get_object_or_404(Page, slug=page_slug)
    return render(request, "pages/show.html", context={"page": page})
