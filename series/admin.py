from django.contrib import admin

from series.models import Series, Seasons, SeasonLota
#from series.models import AssessmentSeason, LearningCourseSeason, ItemSeason, QuadGameSeason
from series.models import AssessmentSeason

admin.site.register(Series)
admin.site.register(Seasons)
admin.site.register(AssessmentSeason)
#admin.site.register(LearningCourseSeason)
#admin.site.register(ItemSeason)
admin.site.register(SeasonLota)
