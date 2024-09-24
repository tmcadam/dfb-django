from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit

from biographies.models import Biography

class Image (models.Model):

    title = models.CharField()
    caption = models.TextField()
    attribution = models.CharField(null=True)
    biography = models.ForeignKey(Biography, on_delete=models.CASCADE)
    image = ProcessedImageField(upload_to='images',
                                           processors=[ResizeToFit(800,800)],
                                           format='JPEG',
                                           options={'quality': 90})
    image300x300 = ImageSpecField(source='image',
                                      processors=[ResizeToFit(300,300)],
                                      format='JPEG',
                                      options={'quality': 90})
    image100x100 = ImageSpecField(source='image',
                                      processors=[ResizeToFit(100,100)],
                                      format='JPEG',
                                      options={'quality': 90})


    def __str__(self):

        return self.title