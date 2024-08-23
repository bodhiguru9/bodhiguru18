from django.contrib import admin
from orgss.models import Org, SubOrg, Role, Weightage

admin.site.register(Org)
admin.site.register(SubOrg)
admin.site.register(Role)
admin.site.register(Weightage)