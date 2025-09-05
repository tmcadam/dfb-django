import secrets

from django.db import models

from biographies.models import Biography


class Comment(models.Model):
    biography = models.ForeignKey(
        Biography, on_delete=models.CASCADE, related_name="comments"
    )
    name = models.CharField(help_text="Name displayed with the comment (required).")
    email = models.EmailField(
        null=False, help_text="This will not be displayed publically (required)."
    )
    comment = models.TextField(null=False)
    approved = models.BooleanField(default=False)
    approve_key = models.CharField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_approve_key(self):
        self.approve_key = secrets.token_urlsafe(16)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.comment[:20]}..."
