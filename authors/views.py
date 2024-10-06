from django.views.generic import ListView
from authors.models import Author

class AuthorsListView(ListView):
    model = Author
