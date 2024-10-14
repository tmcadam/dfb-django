from django.db import models

from biographies.models import Biography

class Comment(models.Model):

    biography = models.ForeignKey(Biography, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, null=False)
    email = models.EmailField(null=False)
    comment = models.TextField(null=False)
    approved = models.BooleanField(default=False)
    approve_key = models.CharField(max_length=16, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.comment[:20]}..."