import re

from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit

from biographies.models import Biography
from common.html_cleaners import clean_urls

class Downsize:

    def __init__(self, size):
        self.size = size

    def process(self, image):
        if image.height > self.size or image.width > self.size:
            return ResizeToFit(self.size, self.size).process(image)
        return image

class Image (models.Model):

    title = models.CharField()
    caption = models.TextField()
    attribution = models.CharField(null=True, blank=True)
    biography = models.ForeignKey(Biography, on_delete=models.CASCADE, related_name="images")
    image = ProcessedImageField(upload_to='images',
                                           processors=[Downsize(800)],
                                           format='JPEG',
                                           options={'quality': 90})
    image300x300 = ImageSpecField(source='image',
                                      processors=[Downsize(300)],
                                      format='JPEG',
                                      options={'quality': 90})
    image100x100 = ImageSpecField(source='image',
                                      processors=[Downsize(100)],
                                      format='JPEG',
                                      options={'quality': 90})

    def save(self, *args, **kwargs):
        self.caption = clean_urls(self.caption)
        super().save(*args, **kwargs)

    @property
    def orientation(self):
        ratio = self.image.width / self.image.height
        if ratio > 0.65 and ratio <= 0.85:
            return "portrait"
        elif ratio >= 1.15:
            return "landscape" 
        elif ratio > 0.85 and ratio < 1.15:   
            return "square"
        else:
            return "other"

    def __str__(self):
        return self.title