from django.db import models

from common.html_cleaners import clean_urls

class Biography(models.Model):

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=50, db_index=True, unique=True)
    lifespan = models.CharField(max_length=50, null=True, blank=True)
    body = models.TextField()
    authors = models.CharField(max_length=250, null=True, blank=True)
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

    @property
    def featured_image_url(self):
        return self.images.order_by("id").first().image300x300.url

    def save(self, *args, **kwargs):
        self.body = clean_urls(self.body)
        super().save(*args, **kwargs)

    def __str__(self):
        if self.lifespan:
            return "{} ({})".format(self.title, self.lifespan)
        return self.title


class Country(models.Model):

    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name
    

