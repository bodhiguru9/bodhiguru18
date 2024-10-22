from django.contrib import admin

from zola.models import Item, Suggestion, ItemResult, LibraryFilter

admin.site.register(Item)
admin.site.register(Suggestion)
admin.site.register(ItemResult)
admin.site.register(LibraryFilter)
