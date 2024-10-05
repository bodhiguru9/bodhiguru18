from django.contrib import admin
from .models import Upgrade, Upgradedetail, UpgradeAssessment

admin.site.register(Upgrade)
admin.site.register(Upgradedetail)
admin.site.register(UpgradeAssessment)