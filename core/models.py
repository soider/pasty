# -*- coding: utf-8 -*-

import os
import re
import random
from urlparse import urlparse
from django.db import models

MAX_IN_BATCH = 30

class Pasty(models.Model):


    class Meta:
        verbose_name = u'Пирожок'
        verbose_name_plural = u'Пирожки'

    text = models.TextField(u'Текст пирожка')
    date = models.DateTimeField(u'Дата публикации', blank=True, null=True)
    source = models.URLField(u'Источник', blank=True)
    votes = models.IntegerField(u'Голосов', default=0, null=True)
    published = models.BooleanField(u'Опубликовано', default=False, null=False)
    source_pattern = re.compile(r'''http://(?:www\.)?(.+)''')

    def short_text(self):
        return self.text[:37].replace(os.linesep, ' \ ') + '...'

    def source_title(self):
        return urlparse(self.source).hostname

    def __unicode__(self):
        return self.short_text()

    @staticmethod
    def rnd():
        pasties = list(Pasty.objects.filter(published=True).order_by('?')[0:MAX_IN_BATCH])
        counter = 0
        upper_limit = sum(pasty.votes for pasty in pasties)
        random_limit = random.uniform(0, upper_limit)
        for pasty in pasties:
            if counter + pasty.votes >= random_limit:
                return pasty
            else:
                counter += pasty.votes
        return None



class Source(models.Model):

    class Meta:
        verbose_name = u'Источник'
        verbose_name_plural = u'Источники'

    title = models.TextField(u'Название источника')
    url = models.URLField(u'Ссылка')
    sync_url = models.URLField(u'URL синхронизации', blank=True)
    sync_date = models.DateTimeField(u'Дата последней синхронизации', blank=True, null=True)
    parser_pattern = re.compile('[.-]')

    def __unicode__(self):
        return self.title

    def parser_key(self):
        return self.parser_pattern.sub('_', self.title)
