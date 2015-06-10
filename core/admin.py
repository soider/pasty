# -*- coding: utf-8 -*-
import datetime

from django.contrib import admin
from core.models import Pasty, Source


class PastyAdmin(admin.ModelAdmin):
    list_display = ('date', 'source', 'short_text', 'votes', 'published')
    list_filter = ('date', 'source')
    search_fields = ('text', )
    date_hierarchy = 'date'
    fields = ('date', 'source', 'text', 'published')

    def publish(modeladmin, request, queryset):
        try:
            queryset.update(published=True,
                        date=datetime.datetime.now())
        except Exception: # Это считается плохой практикой, но, кажется, это будет лучше чем сломать админку.
            import traceback
            error_message = u"Не удалось опубликовать пирожки: %s" % traceback.format_exc()
            modeladmin.message_user(request, error_message, level='ERROR')
    publish.short_description = "Make published"

    actions = [publish]


class SourceAdmin(admin.ModelAdmin):

    list_display = ('title', 'url', 'sync_date', )
    search_fields = ('text', )
    fields = ('title', 'url', 'sync_url', )


admin.site.register(Pasty, PastyAdmin)

admin.site.register(Source, SourceAdmin)