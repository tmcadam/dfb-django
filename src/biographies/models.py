from django.db import models

class Biography(models.Model):

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=50, db_index=True, unique=True)
    lifespan = models.CharField(max_length=50, null=True)
    body = models.TextField()
    authors = models.CharField(max_length=250, null=True)
    revisions = models.TextField(null=True)
    external_links = models.TextField(null=True)
    references = models.TextField(null=True)
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