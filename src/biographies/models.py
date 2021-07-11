from django.db import models

class Biography(models.Model):

    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=50, db_index=True, unique=True)
    lifespan = models.CharField(max_length=50)
    body = models.TextField()
    authors = models.CharField(max_length=250)
    revisions = models.TextField()
    external_links = models.TextField()
    references = models.TextField()
    primary_country = models.ForeignKey('Country', on_delete=models.PROTECT, null=True, related_name='+')
    secondary_country = models.ForeignKey('Country', on_delete=models.PROTECT, null=True, related_name='+')
    south_georgia = models.BooleanField()
    featured = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]
        verbose_name_plural = "Biographies"


class Country(models.Model):

    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Countries"