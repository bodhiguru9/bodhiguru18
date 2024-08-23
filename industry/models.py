from django.db import models

class Industry(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length = 100, null=True, blank=True)
    description = models.CharField(max_length = 500, blank=True, null=True)