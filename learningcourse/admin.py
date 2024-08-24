from django.contrib import admin

from learningcourse.models import LearningCourse, LearningCourseDocument, LearningCourseVideo

admin.site.register(LearningCourse)
admin.site.register(LearningCourseDocument)
admin.site.register(LearningCourseVideo)
