from django.db import models

from common.html_cleaners import clean_urls
from biographies.images_helper import interlace_images

class Biography(models.Model):

    title = models.CharField(db_index=True)
    slug = models.SlugField(db_index=True, unique=True)
    lifespan = models.CharField(null=True, blank=True)
    body = models.TextField()
    authors = models.CharField(null=True, blank=True)
    revisions = models.TextField(null=True, blank=True)
    external_links = models.TextField(null=True, blank=True)
    references = models.TextField(null=True, blank=True)
    primary_country = models.ForeignKey('Country', on_delete=models.PROTECT, null=True, blank=True, related_name='+')
    secondary_country = models.ForeignKey('Country', on_delete=models.PROTECT, null=True, blank=True, related_name='+')
    south_georgia = models.BooleanField()
    featured = models.BooleanField()
    authors_connections = models.ManyToManyField('authors.Author', through='authors.BiographyAuthor', related_name="biographies")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]
        verbose_name_plural = "Biographies"

    def body_with_images(self):
        return interlace_images(self)

    def get_ordered_authors(self):
        return self.authors_connections.all().order_by('biographyauthor__author_position')

    def approved_comments(self):
        return self.comments.filter(approved=True).order_by('created_at')

    @property
    def featured_image_url(self):
        return self.images.order_by("id").first().image300x300.url

    def save(self, *args, **kwargs):
        self.body = clean_urls(self.body)
        if self.authors:
            self.authors = self.authors.strip()
        if self.external_links:
            self.external_links = self.external_links.strip()
        if self.references:
            self.references = self.references.strip()
        if self.revisions:
            self.revisions = self.revisions.strip()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.lifespan:
            return "{} ({})".format(self.title, self.lifespan)
        return self.title


class Country(models.Model):

    name = models.CharField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


