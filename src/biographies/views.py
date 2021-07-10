from django.shortcuts import render
from django.conf import settings

# Create your views here.
def home(request):
    context = {'env':settings.ENVIRONMENT}
    return render(request, 'main/home.html', context)