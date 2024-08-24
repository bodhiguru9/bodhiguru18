
# Register your models here.
from django.contrib import admin

from assessments.models import Question, Option, AssessmentType
from assessments.models import Assessment, AssessmentResult

admin.site.register(Question)
admin.site.register(Option)
admin.site.register(AssessmentType)
admin.site.register(Assessment)
admin.site.register(AssessmentResult)
