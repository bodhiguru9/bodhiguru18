from django.db import models

from accounts.models import Account
from series.models import Series
from series.models import AssessmentSeason, LearningCourseSeason
#from series.models import AssessmentSeason, ItemSeason, LearningCourseSeason
from learningcourse.models import LearningCourse, LearningCourseVideo, LearningCourseDocument

class SeriesAssignUser(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    progress = models.IntegerField(default=0)

    class Meta:
        unique_together = ["user", "series"]

    def __str__(self):
        return f"{self.user.username} - {self.series.name}"

class AssessmentProgress(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    assessment_season = models.ForeignKey(AssessmentSeason, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ["user", "assessment_season"]

    def __str__(self):
        return f"{self.user.username} - {self.assessment_season.season.name}"
"""
class ItemProgress(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    item_season = models.ForeignKey(ItemSeason, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ["user", "item_season"]

    def __str__(self):
        return f"{self.user.username} - {self.item_season.season.name} - {self.item_season.item.item_name}"
"""