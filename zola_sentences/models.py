from django.db import models
from zola.models import Item


# Create your models here.

class Sentences(models.Model):

    def __str__(self):
        return f"{self.sentence} - {self.item}"

    sentence = models.CharField(max_length=256, null=True, blank=True)
    item = item = models.ForeignKey(Item, on_delete=models.CASCADE, default="sentences")