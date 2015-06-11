# -*- coding: utf-8 -*-
from __future__ import absolute_import

from celery import Task

from core.models import Source
from core.sync import sync_rss_source, SyncError


class SyncTask(Task):
    """Synchronize :Source: with :src_id:"""

    max_retries = 2

    def run(self, src_id):
        try:
            source = Source.objects.get(pk=src_id)
            sync_rss_source(source)
        except SyncError:
            self.retry(src_id)