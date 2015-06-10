# -*- coding: utf-8 -*-
from __future__ import absolute_import

from celery import shared_task


@shared_task
def sync(sync_id):
    print "Will sync", sync_id