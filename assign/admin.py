from django.contrib import admin

from assign.models import SeriesAssignUser
#from assign.models import AssessmentProgress, ItemProgress
from assign.models import AssessmentProgress

admin.site.register(SeriesAssignUser)
admin.site.register(AssessmentProgress)
#admin.site.register(ItemProgress)
