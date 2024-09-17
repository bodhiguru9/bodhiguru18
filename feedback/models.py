from django.db import models

# Create your models here.


class Feedback(models.Model):
    email = models.EmailField(max_length=70)
    contact_number = models.CharField(max_length=15, default= 1234567890)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.email} - {self.description}"