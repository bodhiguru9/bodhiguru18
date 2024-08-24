from django.contrib import admin
from .models import UserSubOrgs, UserMapping, UserRights, UserRightsMapping
# Register your models here.

admin.site.register(UserSubOrgs)
admin.site.register(UserMapping)
admin.site.register(UserRights)
admin.site.register(UserRightsMapping)