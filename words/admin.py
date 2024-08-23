from django.contrib import admin
from .models import Words, PowerWords, NegativeWords, EmotionWords

# Register your models here.

admin.site.register(Words)
admin.site.register(PowerWords)
admin.site.register(NegativeWords)
admin.site.register(EmotionWords)