# *-* coding: utf-8 *-*

from django.apps import AppConfig

class PastyCoreConfig(AppConfig):
    name = 'core'
    verbose_name = u"Пирожки"


default_app_config = 'core.PastyCoreConfig'
