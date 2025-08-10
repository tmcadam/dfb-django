from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from .models import Biography
from .pagination_helper import generate_pagination_links
from comments.forms import SubmitCommentForm

# Create your views here
def index(request):

    search_term = request.GET.get('search', None)
    page_number = request.GET.get("page")

    if search_term:
        biographies = Biography.objects.filter(title__icontains=search_term)
    else:
        search_term = ""
        biographies = Biography.objects.all()

    paginator = Paginator(biographies, 25)
    page_obj = paginator.get_page(page_number)
    page_obj.pagination_links = generate_pagination_links(page_obj.number, paginator.num_pages)

    return render(request, 'biographies/index.html', {"page_obj": page_obj, "search_term": search_term})

def show(request, bio_slug):
    biography = get_object_or_404(Biography, slug=bio_slug)
    comments_form = SubmitCommentForm(initial={"biography": biography.id})
    return render(request, 'biographies/show.html', {'biography': biography, 'comments_form': comments_form})
