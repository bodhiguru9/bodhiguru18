from django.db import models

from words.models import PowerWords, NegativeWords, EmotionWords


class Senti(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=250, unique=True)


class Sub_Competency(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=250, unique=True)
    power_words = models.ManyToManyField(PowerWords, blank=True)
    negative_words = models.ManyToManyField(NegativeWords, blank=True)
    emotion_words = models.ManyToManyField(EmotionWords, blank=True)

    

class Competency(models.Model):
    def __str__(self):
        return self.competency_name

    competency_name = models.CharField(max_length = 250, unique=True)
    sub_competency = models.ManyToManyField(Sub_Competency, blank=True)
    competency_sentiment = models.ManyToManyField(Senti, blank=True)

    def get_senti_as_string(self):
        return ', '.join(self.competency_sentiment.values_list('name', flat=True))


class MasterCompetency(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=250, unique=True)
    master_competency = models.ManyToManyField(Competency, blank = True)
