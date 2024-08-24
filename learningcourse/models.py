from django.db import models

from orgss.models import SubOrg

class LearningCourse(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    thumbnail = models.FileField(upload_to="media/learningcourse/thumbnail", null=True, blank=True)
    sub_org = models.ForeignKey(SubOrg, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class LearningCourseVideo(models.Model):
    course = models.ForeignKey(LearningCourse, on_delete=models.CASCADE)
    video = models.FileField(upload_to="media/learningcourse/video")
    
    def __str__(self):
        return f"{self.course.name} - {self.video.url}"

class LearningCourseDocument(models.Model):
    course = models.ForeignKey(LearningCourse, on_delete=models.CASCADE)
    document = models.FileField(upload_to="media/learningcourse/document")
    
    def __str__(self):
        return f"{self.course.name} - {self.document.url}"
