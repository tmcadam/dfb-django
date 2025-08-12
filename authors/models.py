from django.db import models
from django.utils.text import slugify

from biographies.models import Biography
from common.html_cleaners import clean_urls

class Author(models.Model):

    first_name = models.CharField(null=True)
    last_name = models.CharField()
    biography = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('first_name', 'last_name')
        ordering = ["last_name", "first_name"]

    @property
    def name(self):
        formatted_first_name = f"{self.first_name} " if self.first_name else ""
        return formatted_first_name + self.last_name

    @property
    def simple_slug(self):
        return slugify(self.name)

    def __str__(self):
        formatted_first_name = f", {self.first_name}" if self.first_name else ""
        return self.last_name + formatted_first_name

    @property
    def short_biography(self):
        if not self.biography:
            return "No biography available."

        if len(self.biography) > 100:
            return self.biography[:100] + "..."
        return self.biography



class BiographyAuthor(models.Model):

    biography = models.ForeignKey(Biography, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    author_position = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('biography', 'author'),
                           ('biography', 'author_position')]
        ordering = ["author_position"]

    def __str__(self):
        return f"#{self.id}"
