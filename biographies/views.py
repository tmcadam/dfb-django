import json
import random
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, UpdateView
from django.views.generic.edit import DeleteView

from .forms import BiographyForm, BiographyAuthorFormSet
from .models import Biography, Country
from .pagination_helper import generate_pagination_links
from .featured_helper import reset_featured_bios
from .link_checker import check_links_in_bios
from comments.forms import SubmitCommentForm
from authors.models import Author


# Create your views here
def index(request):
    search_term = request.GET.get("search", None)
    page_number = request.GET.get("page")

    if search_term:
        biographies = Biography.objects.filter(title__icontains=search_term)
    else:
        search_term = ""
        biographies = Biography.objects.all()

    paginator = Paginator(biographies, 25)
    page_obj = paginator.get_page(page_number)
    page_obj.pagination_links = generate_pagination_links(
        page_obj.number, paginator.num_pages
    )

    return render(
        request,
        "biographies/index.html",
        {"page_obj": page_obj, "search_term": search_term},
    )


def show_by_slug(request, bio_slug):
    biography = get_object_or_404(Biography, slug=bio_slug)
    comments_form = SubmitCommentForm(initial={"biography": biography.id})
    return render(
        request,
        "biographies/show.html",
        {"biography": biography, "comments_form": comments_form},
    )


def show_by_id(request, bio_id):
    biography = get_object_or_404(Biography, id=bio_id)
    return redirect("biographies:show", bio_slug=biography.slug)


class BiographyCreateView(LoginRequiredMixin, CreateView):
    model = Biography
    form_class = BiographyForm
    template_name = "biographies/form.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["authors_formset"] = BiographyAuthorFormSet(self.request.POST)
        else:
            data["authors_formset"] = BiographyAuthorFormSet()
        # Pass existing authors as JSON for populating new dropdowns
        all_authors = list(Author.objects.values("id", "first_name", "last_name"))
        data["existing_authors_json"] = json.dumps(all_authors)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        authors_formset = context["authors_formset"]
        if form.is_valid() and authors_formset.is_valid():
            self.object = form.save()
            authors_formset.instance = self.object
            authors_formset.save()
            return super().form_valid(form)
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy("biographies:show", kwargs={"bio_slug": self.object.slug})


class BiographyUpdateView(LoginRequiredMixin, UpdateView):
    model = Biography
    form_class = BiographyForm
    template_name = "biographies/form.html"
    slug_url_kwarg = "bio_slug"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["authors_formset"] = BiographyAuthorFormSet(
                self.request.POST, instance=self.object
            )
        else:
            data["authors_formset"] = BiographyAuthorFormSet(instance=self.object)
        # Pass existing authors as JSON for populating new dropdowns
        data["existing_authors_json"] = json.dumps(
            list(Author.objects.values("id", "first_name", "last_name"))
        )
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        authors_formset = context["authors_formset"]
        if form.is_valid() and authors_formset.is_valid():
            self.object = form.save()
            authors_formset.instance = self.object
            authors_formset.save()
            return super().form_valid(form)
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy("biographies:show", kwargs={"bio_slug": self.object.slug})


@login_required
def reset_featured(request):
    reset_featured_bios()
    messages.success(request, "Featured biographies reset successful")
    return redirect("pages:home")


@login_required
def check_links(request):
    links_result = check_links_in_bios()
    context = {"fails": links_result["fails"], "count": links_result["count"]}
    return render(request, "biographies/check_links.html", context)


@login_required
def manage_biographies(request):
    search_term = request.GET.get("search", "")
    page_number = request.GET.get("page", 1)

    if search_term:
        biographies = Biography.objects.filter(title__icontains=search_term)
    else:
        biographies = Biography.objects.all()

    paginator = Paginator(biographies, 25)
    page_obj = paginator.get_page(page_number)

    # HTMX response check
    if request.headers.get("HX-Request"):
        return render(
            request,
            "biographies/_manage_table.html",
            {"page_obj": page_obj, "search_term": search_term},
        )

    return render(
        request,
        "biographies/manage.html",
        {"page_obj": page_obj, "search_term": search_term},
    )


class BiographyDeleteView(LoginRequiredMixin, DeleteView):
    model = Biography
    template_name = "biographies/delete.html"
    success_url = reverse_lazy("biographies:manage")
    slug_url_kwarg = "bio_slug"


@login_required
def make_featured(request, bio_slug):
    biography = get_object_or_404(Biography, slug=bio_slug)

    if not biography.featured:
        current_featured = list(Biography.objects.filter(featured=True))

        if len(current_featured) >= 6:
            bio_to_remove = random.choice(current_featured)
            bio_to_remove.featured = False
            bio_to_remove.save()

        biography.featured = True
        biography.save()
        messages.success(
            request, f'"{biography.title}" has been set as a featured biography.'
        )

    return redirect(request.META.get("HTTP_REFERER", "biographies:manage"))


@login_required
def validate_slug(request):
    slug = request.GET.get("slug", "").strip()
    bio_id = request.GET.get("bio_id", "")

    if not slug:
        return HttpResponse("")

    is_valid_format = slug == slugify(slug)
    if not is_valid_format:
        return HttpResponse(
            '<span class="text-danger"><i class="fa fa-times"></i> Invalid format (use lowercase, hyphens)</span>'
        )

    qs = Biography.objects.filter(slug=slug)
    if bio_id:
        qs = qs.exclude(pk=bio_id)

    if qs.exists():
        return HttpResponse(
            '<span class="text-danger"><i class="fa fa-times"></i> Slug is already in use</span>'
        )

    return HttpResponse(
        '<span class="text-success"><i class="fa fa-check"></i> Slug is available!</span>'
    )


@login_required
@require_POST
def add_country_htmx(request):
    country_name = request.POST.get("name", "").strip()
    target_field = request.POST.get("target_field", "")

    curr_primary = request.POST.get("primary_country", "")
    curr_secondary = request.POST.get("secondary_country", "")

    if country_name:
        country_exists = Country.objects.filter(name__iexact=country_name).first()

        if country_exists:
            return HttpResponse(
                f'<span class="text-danger"><i class="fa fa-exclamation-triangle"></i> "{country_exists.name}" already exists!</span>'
            )

        country = Country.objects.create(name=country_name)

        if target_field == "id_primary_country":
            curr_primary = str(country.id)
        elif target_field == "id_secondary_country":
            curr_secondary = str(country.id)

        def render_options(selected_val):
            html = '<option value="">---------</option>\n'
            # Country model handles alphabetical ordering automatically
            for c in Country.objects.all():
                selected = "selected" if str(c.id) == str(selected_val) else ""
                html += f'<option value="{c.id}" {selected}>{c.name}</option>\n'
            return html

        # Completely replacing both selects maintains alphabetical order
        # and doesn't overwrite whichever choice wasn't the target
        response = f"""
        <select name="primary_country" class="select form-control" id="id_primary_country" hx-swap-oob="true">
            {render_options(curr_primary)}
        </select>
        <select name="secondary_country" class="select form-control" id="id_secondary_country" hx-swap-oob="true">
            {render_options(curr_secondary)}
        </select>
        <script>
            $('#addCountryModal').modal('hide');
            $('#addCountryModal form')[0].reset();
            $('#country-error').html('');
        </script>
        """

        return HttpResponse(response)

    return HttpResponse(status=400)


@login_required
@require_POST
def add_author_htmx(request):
    first_name = request.POST.get("first_name", "").strip()
    last_name = request.POST.get("last_name", "").strip()
    target_field = request.POST.get("target_field", "")

    if last_name:
        author_exists = Author.objects.filter(
            first_name__iexact=first_name, last_name__iexact=last_name
        ).first()

        if author_exists:
            return HttpResponse(
                f'<span class="text-danger"><i class="fa fa-exclamation-triangle"></i> "{author_exists.name}" already exists!</span>'
            )

        author = Author.objects.create(first_name=first_name, last_name=last_name)

        response = f'''
        <script>
            var authorName = "{author.name}";
            var authorId = {author.id};
            var newAuthor = {{ id: {author.id}, first_name: "{author.first_name}", last_name: "{author.last_name}" }};

            // Add to EXISTING_AUTHORS array so future "Add Author" rows include this author
            if (typeof EXISTING_AUTHORS !== "undefined") {{
                EXISTING_AUTHORS.push(newAuthor);
            }}

            var selects = document.querySelectorAll('select[name$="-author"]');
            selects.forEach(function(select) {{
                select.appendChild(new Option(authorName, authorId, false, false));
            }});

            var targetField = document.getElementById("{target_field}");
            if (targetField) {{
                targetField.value = authorId;
            }}

            $('#addAuthorModal').modal('hide');
            $('#author_first_name').val('');
            $('#author_last_name').val('');
            $('#author-error').html('');
        </script>
        '''
        return HttpResponse(response)
    return HttpResponse('<span class="text-danger">Last name is required!</span>')
