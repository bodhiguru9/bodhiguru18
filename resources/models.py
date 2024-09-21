from django.db import models

class Resource(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail = models.FileField(upload_to='media/item/thumbnail', null=True, blank=True)  
    youtube_link = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

class TextResouce(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    video = models.URLField(max_length=200, blank=True, null=True, default = 'https://www.youtube.com/watch?v=tfrvVKM0DZY')

    

    def __str__(self):
        return self.name
