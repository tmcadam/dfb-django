from django.shortcuts import render
from biographies.models import Biography

# Create your views here.
def home(request):
    featured_bios = Biography.objects.filter(featured=True)
    return render(request, 'pages/home.html', context={"featured_bios": featured_bios})