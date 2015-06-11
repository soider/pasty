# -*- coding: utf-8 -*-
import datetime

from django.contrib import admin
from django.db import Error as DBError
from core.models import Pasty, Source

import core.tasks


class PastyAdmin(admin.ModelAdmin):
    list_display = ('date', 'source', 'short_text', 'votes', 'published')
    list_filter = ('date', 'source', 'published')
    search_fields = ('text', )
    date_hierarchy = 'date'
    fields = ('date', 'source', 'text', 'published')

    def publish(modeladmin, request, queryset):
        try:
            queryset.update(published=True,
                        date=datetime.datetime.now())
        except DBError:
            import traceback
            error_message = u"Не удалось опубликовать пирожки: %s" % traceback.format_exc()
            modeladmin.message_user(request, error_message, level='ERROR')
    publish.short_description = u"Опубликовать"

    actions = [publish]


class SourceAdmin(admin.ModelAdmin):

    list_display = ('title', 'url', 'sync_date', )
    search_fields = ('text', )
    fields = ('title', 'url', 'sync_url', )

    def sync(modeladmin, request, queryset):
        try:
            for source in queryset:
                core.tasks.SyncTask().delay(source.id)
            modeladmin.message_user(request, u'Синхронизация запущена', level='INFO')
        except Exception:
            import traceback
            error_message = u"Не удалось синхронизировать пирожки: %s" % traceback.format_exc()
            modeladmin.message_user(request, error_message, level='ERROR')

    sync.short_description = u'Запустить синхронизацию'

    actions = [sync]


admin.site.register(Pasty, PastyAdmin)
admin.site.register(Source, SourceAdmin)
