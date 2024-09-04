from django.db import models

class Resource(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    youtube_link = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name