from django.db import models
from django.utils.text import slugify


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
    authors_connections = models.ManyToManyField('Author', through='BiographyAuthor', related_name="biographies")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]
        verbose_name_plural = "Biographies"

    def __str__(self):
        if self.lifespan:
            return "{} ({})".format(self.title, self.lifespan)
        return self.title


class Author(models.Model):

    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50)
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


class BiographyAuthor(models.Model):
    
    biography = models.ForeignKey(Biography, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    author_position = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('biography', 'author'),
                           ('biography', 'author_position')]
        ordering = ["biography", "author_position"]

    def __str__(self):
        return f"#{self.id}"


class Country(models.Model):

    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name
    

class Comment(models.Model):

    biography = models.ForeignKey(Biography, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, null=False)
    email = models.EmailField(null=False)
    comment = models.TextField(null=False)
    approved = models.BooleanField(default=False)
    approve_key = models.CharField(max_length=16, null=True, blank=True)

    def __str__(self):
        return f"{self.comment[:20]}..."