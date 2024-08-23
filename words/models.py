from django.db import models

class Words(models.Model):
    def __str__(self):
        return self.word_name

    word_name = models.CharField(max_length=250)

    def save(self, *args, **kwargs):
        self.word_name = self.word_name.lower()
        super(Words, self).save(*args, **kwargs)

class PowerWords(models.Model):
    def __str__(self):
        return f'{self.word}'
    
    word = models.ForeignKey(Words, on_delete=models.CASCADE, default=1, related_name= 'pww')
    weight = models.IntegerField(default=1)
    sentence = models.CharField(max_length=250, default= "sentence")
    power_word_name = models.CharField(max_length=250, default="pw")

class NegativeWords(models.Model):
    def __str__(self):
         return f'{self.word}'

    
    word = models.ForeignKey(Words, on_delete=models.CASCADE, default=1, related_name= 'nww')
    weight = models.IntegerField(default= -7)
    sentence = models.CharField(max_length=250, default= "sentence")
    negative_word_name = models.CharField(max_length=250, default="ww")


class EmotionWords(models.Model):
    def __str__(self):
        return f'{self.word}'

    word = models.ForeignKey(Words, on_delete=models.CASCADE, default=1, related_name= 'eww')
    emotion_word_name = models.CharField(max_length=250)    
