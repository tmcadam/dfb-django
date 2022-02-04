from django.shortcuts import get_object_or_404, render
from .models import Biography

# Create your views here
def show(request, bio_slug):
    biography = get_object_or_404(Biography, slug=bio_slug)
    return render(request, 'biographies/show.html', {'biography': biography})