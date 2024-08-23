from django.contrib import admin
from .models import Competency, Sub_Competency, MasterCompetency, Senti


# Register your models here.
admin.site.register(Competency)
admin.site.register(Sub_Competency)
admin.site.register(MasterCompetency)
admin.site.register(Senti)